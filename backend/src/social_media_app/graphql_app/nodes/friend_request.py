import strawberry
from .user import UserNode
from datetime import datetime
from social_media_app.schemas import Post, Friend, FriendRequestStatus
from strawberry import relay
from typing import Iterable, List
from sqlalchemy import select
from src.logger import get_logger
logger = get_logger(__name__)

@strawberry.type
class FriendRequestNode(relay.Node):
    friend: UserNode
    friends_at: datetime
    status: FriendRequestStatus

    def resolve_id(self, info: strawberry.Info) -> str:
        # Combine your composite keys into a single string
        # Strawberry will then encode this into a global Relay ID
        logger.info('exit')
        return f"{self.user.id}:{self.friend.id}"

    @classmethod
    async def resolve_nodes(
        cls, *, info: strawberry.Info, node_ids: Iterable[str], required: bool = False
    ) -> List["FriendRequestNode"]:
        # This method is called when refetching via the 'node' query
        # Strawberry automatically decodes the Base64 IDs back to 'int' node_ids
        results = []
        for nid in node_ids:
            uid, fid = nid.split(":")
            data = await FriendRequestNode.get(info, nid)
            if data:
                results.append(FriendRequestNode.from_db(info, data))
        logger.info('exit')
        return results

    @staticmethod
    async def get(info: strawberry.Info, nid):
        uid, fid = nid.split(":")
        db_factory=info.context.db_factory
        async with db_factory() as db:
            statement=select(Friend).where(Friend.user_id==uid, Friend.friend_id==fid)
            result=await db.execute(statement)
            db_user=result.scalar_one_or_none()
            logger.info('exit')
            return db_user
    
    @staticmethod
    def from_db(info: strawberry.Info, db_user:Post)->"FriendRequestNode":
        logger.info('exit')
        return FriendRequestNode(friends_at=db_user.friends_at,
            friend=UserNode.from_db(info, UserNode.get(info, db_user.friend_id)),
            status=db_user.status.value
        )
