import strawberry
from .user import UserNode
from social_media_app.schemas import UserSetting
from strawberry import relay
from typing import Iterable, List
from sqlalchemy import select
from src.logger import get_logger
logger = get_logger(__name__)

@strawberry.type
class UserSettingNode(relay.Node):
    id: relay.NodeID[int]
    user: UserNode
    theme: str

    @classmethod
    async def resolve_nodes(
        cls, *, info: strawberry.Info, node_ids: Iterable[str], required: bool = False
    ) -> List["UserSettingNode"]:
        # This method is called when refetching via the 'node' query
        # Strawberry automatically decodes the Base64 IDs back to 'int' node_ids
        results = []
        for nid in node_ids:
            data = await UserSettingNode.get(info, int(nid))
            if data:
                results.append(UserSettingNode.from_db(data))
        logger.info('exit')
        return results

    @staticmethod
    async def get(info: strawberry.Info, user_id):
        db_factory=info.context.db_factory
        async with db_factory() as db:
            statement=select(UserSetting).where(UserSetting.id==user_id)
            result=await db.execute(statement)
            user_setting = result.scalar_one_or_none()
            logger.info('exit')
            return user_setting
