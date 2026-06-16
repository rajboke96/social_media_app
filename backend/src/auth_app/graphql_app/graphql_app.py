import strawberry
from strawberry.fastapi import GraphQLRouter
from .graphql_mutations import Mutation
from .context_permissions import get_context

@strawberry.type
class Query:
    @strawberry.field
    def ping(self, info: strawberry.Info) -> str:
        return "Pong"
    
# 4. Create the Schema
schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_auth_router = GraphQLRouter(schema, context_getter=get_context, 
                            multipart_uploads_enabled=True # Mandatory for file inputs
                            )