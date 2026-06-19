import strawberry
from strawberry.fastapi import GraphQLRouter
from .graphql_query import Query
from .graphql_mutations import Mutation
from .context_permissions import get_context
from src.logger import get_logger
logger = get_logger(__name__)

# 4. Create the Schema
schema = strawberry.Schema(query=Query, mutation=Mutation)

sm_app_router = GraphQLRouter(schema, context_getter=get_context, 
                            multipart_uploads_enabled=True # Mandatory for file inputs
                            )
