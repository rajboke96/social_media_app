import strawberry
from .user import UserNode
from .media import MediaNode
from datetime import datetime
from social_media_app.schemas import Visibility, Post
from strawberry import relay
from typing import Iterable, List, Optional
from sqlalchemy import select
from src.logger import get_logger
logger = get_logger(__name__)

@strawberry.type
class UserPostNode(relay.Node):
    id: relay.NodeID[int]
    title:str
    description: str|None
    created_by: "UserNode"
    created_at: datetime
    visibility: Visibility
    media: Optional[List[MediaNode]]

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
        logger.info('exit')
        return results

    @staticmethod
    async def get(info: strawberry.Info, id):
        db_factory=info.context.db_factory
        async with db_factory() as db:
            statement=select(Post).where(Post.id==id)
            result=await db.execute(statement)
            db_user=result.scalar_one_or_none()
            logger.info('exit')
            return db_user
    
    @staticmethod
    async def from_db(info: strawberry.Info, db_user:Post)->"UserPostNode":
        return UserPostNode(id=db_user.id,
            title=db_user.title,
            description=db_user.description,
            created_at=db_user.created_at,
            created_by=UserNode.from_db(info, db_user.user),
            visibility=db_user.visibility.value,
            media=[await MediaNode.from_db(info, m) for m in db_user.media] if db_user.media else None
        )
