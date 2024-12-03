from fastapi import APIRouter, Depends
from graphql.execution.executors.asyncio import AsyncioExecutor
from starlette.graphql import GraphQLApp
from starlette.requests import Request

from dependencies.get_async_session import get_async_session
from graphql_schemas import schema
from schemas.user_schema import RequestUserSchema

graphql_router = APIRouter()

graphql_app = GraphQLApp(schema=schema, executor_class=AsyncioExecutor)


@graphql_router.post('/gql')
async def graphql_request_handler(request: Request, session=Depends(get_async_session)):
    user = RequestUserSchema(id='03c9cf55-a7ca-4131-9662-15dadbe79959', username='string')
    request.state.user = user
    request.state.session = session
    return await graphql_app.handle_graphql(request=request)
