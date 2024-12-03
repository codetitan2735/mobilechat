import graphene

from managers.chat_room_manager import ChatRoomManager
from mongodb.services import mongodb_chat_room_service


class Message(graphene.ObjectType):
    text = graphene.String()
    timestamp = graphene.DateTime()
    author_id = graphene.String()


class ChatRoom(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    creator = graphene.String()
    members = graphene.List(graphene.String)
    messages = graphene.List(Message)


class ChatRoomQuery(graphene.ObjectType):
    chat_room = graphene.Field(ChatRoom, chat_room_id=graphene.String(required=True))
    chat_rooms = graphene.List(ChatRoom)

    @staticmethod
    async def resolve_chat_room(parent, info, chat_room_id):
        session = info.context["request"].state.session
        chat_room_manager = ChatRoomManager(session=session)
        chat_room = await chat_room_manager.retrieve(pk=chat_room_id)
        chat_room_messages = await mongodb_chat_room_service.get_chat_room_messages(chat_room_id=chat_room_id)
        return ChatRoom(
            id=chat_room.id,
            name=chat_room.name,
            creator=chat_room.creator,
            members=chat_room.members,
            messages=chat_room_messages
        )

    @staticmethod
    async def resolve_chat_rooms(parent, info):
        session = info.context["request"].state.session
        chat_room_manager = ChatRoomManager(session=session)
        chat_rooms = await chat_room_manager.list()
        chat_room_list = []
        for chat_room in chat_rooms:
            chat_room_messages = await mongodb_chat_room_service.get_chat_room_messages(chat_room_id=str(chat_room.id))
            chat_room_list.append(ChatRoom(
                id=chat_room.id,
                name=chat_room.name,
                creator=chat_room.creator,
                members=chat_room.members,
                messages=chat_room_messages
            ))
        return chat_room_list


class CreateChatRoomInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    members = graphene.List(graphene.NonNull(graphene.String), required=True)


class CreateChatRoom(graphene.Mutation):

    class Arguments:
        chat_room_data = CreateChatRoomInput(required=True)

    chat_room = graphene.Field(ChatRoom)

    @staticmethod
    async def mutate(root, info, chat_room_data):
        session = info.context["request"].state.session
        chat_room_manager = ChatRoomManager(session=session)
        chat_room_data['creator'] = str(info.context["request"].state.user.id)
        chat_room = await chat_room_manager.create(data=chat_room_data)
        await mongodb_chat_room_service.create_chat_room_mongodb(origin_chat_room_id=str(chat_room.id))
        return CreateChatRoom(chat_room=ChatRoom(
            id=chat_room.id,
            name=chat_room.name,
            creator=chat_room.creator,
            members=chat_room.members,
            messages=[]
        ))


class UpdateChatRoomInput(graphene.InputObjectType):
    id = graphene.String(required=True)
    name = graphene.String()
    members = graphene.List(graphene.String)


class UpdateChatRoom(graphene.Mutation):

    class Arguments:
        chat_room_data = UpdateChatRoomInput(required=True)

    chat_room = graphene.Field(ChatRoom)

    @staticmethod
    async def mutate(root, info, chat_room_data):
        session = info.context["request"].state.session
        chat_room_id = chat_room_data.pop('id')
        chat_room_manager = ChatRoomManager(session=session)
        if chat_room_data:
            await chat_room_manager.update(pk=chat_room_id, data=chat_room_data)
        chat_room = await chat_room_manager.retrieve(pk=chat_room_id)
        chat_room_messages = await mongodb_chat_room_service.get_chat_room_messages(chat_room_id=chat_room_id)
        return UpdateChatRoom(chat_room=ChatRoom(
            id=chat_room.id,
            name=chat_room.name,
            creator=chat_room.creator,
            members=chat_room.members,
            messages=chat_room_messages
        ))


class DeleteChatRoom(graphene.Mutation):

    class Arguments:
        chat_room_id = graphene.String(required=True)

    status = graphene.String()

    @staticmethod
    async def mutate(root, info, chat_room_id):
        session = info.context["request"].state.session
        chat_room_manager = ChatRoomManager(session=session)
        await chat_room_manager.delete(pk=chat_room_id)
        return DeleteChatRoom(status=f'Chat room with id {chat_room_id} deleted')


class ChatRoomMutation(graphene.ObjectType):
    create_chat_room = CreateChatRoom.Field()
    update_chat_room = UpdateChatRoom.Field()
    delete_chat_room = DeleteChatRoom.Field()
