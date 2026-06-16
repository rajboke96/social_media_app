import strawberry
from .user import UserNode
from datetime import datetime
from social_media_app.schemas import Visibility, Post
from strawberry import relay
from typing import Iterable, List
from sqlalchemy import select

@strawberry.type
class UserPostNode(relay.Node):
    id: relay.NodeID[int]
    title:str
    description: str|None
    created_by: "UserNode"
    created_at: datetime
    visibility: Visibility

    @classmethod
    async def resolve_nodes(
        cls, *, info: strawberry.Info, node_ids: Iterable[str], required: bool = False
    ) -> List["UserPostNode"]:
        # This method is called when refetching via the 'node' query
        # Strawberry automatically decodes the Base64 IDs back to 'int' node_ids
        results = []
        for nid in node_ids:
            data = await UserPostNode.get(info, int(nid))
            if data:
                results.append(UserPostNode.from_db(info, data))
        return results

    @staticmethod
    async def get(info: strawberry.Info, id):
        db_factory=info.context.db_factory
        async with db_factory() as db:
            statement=select(Post).where(Post.id==id)
            result=await db.execute(statement)
            db_user=result.scalar_one_or_none()
            return db_user
    
    @staticmethod
    def from_db(info: strawberry.Info, db_user:Post)->"UserPostNode":
        return UserPostNode(id=db_user.id,
            title=db_user.title,
            description=db_user.description,
            created_at=db_user.created_at,
            created_by=UserNode.from_db(info, UserNode.get(info, db_user.created_by)),
            visibility=db_user.visibility.value
        )