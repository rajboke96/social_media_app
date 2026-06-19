import strawberry
from typing import Optional
from .user import UserNode
from ..graphql_types import CityType
from social_media_app.schemas import UserProfile
from strawberry import relay
from typing import Iterable, List
from sqlalchemy import select
from src.logger import get_logger
logger = get_logger(__name__)

@strawberry.type
class UserProfileNode(relay.Node):
    id: relay.NodeID[int]
    user: Optional["UserNode"]
    profile_bio: str|None
    profile_pic_img: str|None
    cover_pic_img: str|None
    city: Optional["CityType"]

    @classmethod
    async def resolve_nodes(
        cls, *, info: strawberry.Info, node_ids: Iterable[str], required: bool = False
    ) -> List["UserProfileNode"]:
        # This method is called when refetching via the 'node' query
        # Strawberry automatically decodes the Base64 IDs back to 'int' node_ids
        results = []
        for nid in node_ids:
            data = await UserProfileNode.get(info, int(nid))
            if data:
                results.append(UserProfileNode.from_db(data))
        logger.info('exit')
        return results

    async def get(info: strawberry.Info, user_id):
        db_factory=info.context.db_factory
        async with db_factory() as db:
            statement=select(UserProfile).where(UserProfile.user_id==user_id).first()
            result=await db.execute(statement)
            db_city=result.scalar_one_or_none()
            logger.info('exit')
            return db_city
        
    @staticmethod
    def from_db(info: strawberry.Info, db_user:UserProfile)->"UserProfileNode":
        logger.info('exit')
        return UserProfileNode(id=db_user.id,
            user=UserNode.from_db(info, UserNode.get(info, db_user.user_id)) if db_user.user_id else None,
            profile_bio=db_user.profile_bio,
            profile_pic_img=db_user.profile_pic_img,
            cover_pic_img=db_user.cover_pic_img,
            city=CityType.from_db(info, CityType.get(info, db_user.city_id)) if db_user.city_id else None
        )
