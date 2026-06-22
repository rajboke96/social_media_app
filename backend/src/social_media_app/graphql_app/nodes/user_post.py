import strawberry
from .user import UserNode
from .media import MediaNode
from .comment import CommentNode
from datetime import datetime
from social_media_app.schemas import Visibility, Post
from strawberry import relay
from typing import Iterable, List, Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
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
    like_count: int
    comment_count: int
    comments: Optional[List["CommentNode"]]

    @classmethod
    async def resolve_nodes(
        cls, *, info: strawberry.Info, node_ids: Iterable[str], required: bool = False
    ) -> List["UserPostNode"]:
        results = []
        for nid in node_ids:
            data = await UserPostNode.get(info, int(nid))
            if data:
                results.append(await UserPostNode.from_db(info, data))
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
        from sqlalchemy import select, func
        from social_media_app.schemas import Like, Comment
        db_factory = info.context.db_factory
        async with db_factory() as db:
            like_count_stmt = select(func.count(Like.id)).where(Like.post_id == db_user.id)
            like_count_result = await db.execute(like_count_stmt)
            like_count = like_count_result.scalar() or 0

            comment_count_stmt = select(func.count(Comment.id)).where(Comment.post_id == db_user.id)
            comment_count_result = await db.execute(comment_count_stmt)
            comment_count = comment_count_result.scalar() or 0

            comments_stmt = (
                select(Comment)
                .where(Comment.post_id == db_user.id)
                .options(selectinload(Comment.user))
                .order_by(Comment.created_at.desc())
                .limit(20)
            )
            comments_result = await db.execute(comments_stmt)
            comments_db = comments_result.scalars().all()
            comments = [CommentNode.from_db(info, c) for c in comments_db]

            return UserPostNode(
                id=db_user.id,
                title=db_user.title,
                description=db_user.description,
                created_at=db_user.created_at,
                created_by=UserNode.from_db(info, db_user.user),
                visibility=db_user.visibility.value,
                media=[await MediaNode.from_db(info, m) for m in db_user.media] if db_user.media else None,
                like_count=like_count,
                comment_count=comment_count,
                comments=comments if comments else None
            )
