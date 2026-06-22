import strawberry
from .user import UserNode
from datetime import datetime
from src.logger import get_logger
from sqlalchemy import select
from typing import Iterable, List, Optional
from strawberry import relay
from social_media_app.schemas import Comment
from sqlalchemy.orm import selectinload
logger = get_logger(__name__)

@strawberry.type
class CommentNode(relay.Node):
    id: relay.NodeID[int]
    text: str
    created_at: datetime
    user: "UserNode"

    @classmethod
    async def resolve_nodes(
        cls, *, info: strawberry.Info, node_ids: Iterable[str], required: bool = False
    ) -> List["CommentNode"]:
        results = []
        for nid in node_ids:
            data = await CommentNode.get(info, int(nid))
            if data:
                results.append(CommentNode.from_db(info, data))
        logger.info('exit')
        return results

    @staticmethod
    async def get(info: strawberry.Info, id):
        db_factory = info.context.db_factory
        async with db_factory() as db:
            statement = select(Comment).where(Comment.id == id).options(selectinload(Comment.user))
            result = await db.execute(statement)
            db_comment = result.scalar_one_or_none()
            logger.info('exit')
            return db_comment

    @staticmethod
    def from_db(info: strawberry.Info, db_comment: Comment) -> "CommentNode":
        return CommentNode(
            id=db_comment.id,
            text=db_comment.text,
            created_at=db_comment.created_at,
            user=UserNode.from_db(info, db_comment.user),
        )
