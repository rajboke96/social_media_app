import strawberry
from typing import Optional
from .user import UserNode
from .media import MediaNode
from ..graphql_types import CityType
from social_media_app.schemas import UserProfile
from strawberry import relay
from typing import Iterable, List
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.logger import get_logger
logger = get_logger(__name__)

@strawberry.type
class UserProfileNode(relay.Node):
    id: relay.NodeID[int]
    user: Optional["UserNode"]
    profile_bio: str|None
    profile_pic: Optional["MediaNode"]
    cover_pic: Optional["MediaNode"]
    city: Optional["CityType"]

    @classmethod
    async def resolve_nodes(
        cls, *, info: strawberry.Info, node_ids: Iterable[str], required: bool = False
    ) -> List["UserProfileNode"]:
        results = []
        for nid in node_ids:
            data = await UserProfileNode.get(info, int(nid))
            if data:
                results.append(UserProfileNode.from_db(info, data))
        logger.info('exit')
        return results

    async def get(info: strawberry.Info, user_id):
        db_factory=info.context.db_factory
        async with db_factory() as db:
            statement=select(UserProfile).where(UserProfile.user_id==user_id).options(
                selectinload(UserProfile.profile_picture),
                selectinload(UserProfile.cover_picture),
                selectinload(UserProfile.user),
                selectinload(UserProfile.city)
            )
            result=await db.execute(statement)
            db_profile=result.scalar_one_or_none()
            logger.info('exit')
            return db_profile
        
    @staticmethod
    def from_db(info: strawberry.Info, db_user:UserProfile)->"UserProfileNode":
        logger.debug('Inside from_db of UserProfileNode')
        return UserProfileNode(id=db_user.id,
            user=UserNode.from_db(info, db_user.user) if db_user.user else None,
            profile_bio=db_user.profile_bio,
            profile_pic=MediaNode.from_db(info, db_user.profile_picture) if db_user.profile_picture else None,
            cover_pic=MediaNode.from_db(info, db_user.cover_picture) if db_user.cover_picture else None,
            city=CityType.from_db(info, CityType.get(info, db_user.city_id)) if db_user.city_id else None
        )
