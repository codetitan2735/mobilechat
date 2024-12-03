import graphene

from graphql_schemas.char_room_schema import ChatRoomQuery, ChatRoomMutation

schema = graphene.Schema(query=ChatRoomQuery, mutation=ChatRoomMutation)
