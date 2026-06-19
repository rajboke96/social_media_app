import strawberry
from social_media_app.schemas import User as UserModel
from typing import List, Iterable
from strawberry import relay
from sqlalchemy import select
from src.logger import get_logger
logger = get_logger(__name__)

@strawberry.type
class UserNode(relay.Node):
    id: relay.NodeID[int]
    name: str
    email: str|None
    username: str
    account_type: str
    account_status: str

    @classmethod
    async def resolve_nodes(
        cls, *, info: strawberry.Info, node_ids: Iterable[str], required: bool = False
    ) -> List["UserNode"]:
        # This method is called when refetching via the 'node' query
        # Strawberry automatically decodes the Base64 IDs back to 'int' node_ids
        results = []
        for nid in node_ids:
            data = await UserNode.get(info, int(nid))
            if data:
                results.append(UserNode.from_db(info, data))
        logger.info('exit')
        return results
    
    @staticmethod
    async def get(info: strawberry.Info, id):
        db_factory=info.context.db_factory
        async with db_factory() as db:
            statement=select(UserModel).where(UserModel.id==id)
            result=await db.execute(statement)
            db_user=result.scalar_one_or_none()
            logger.info('exit')
            return db_user

    @staticmethod
    def from_db(info: strawberry.Info, db_user:UserModel)->"UserNode":
        logger.info('exit')
        return UserNode(id=db_user.id, 
            name=db_user.firstname, 
            email=db_user.email_address, 
            username=db_user.username,
            account_type=db_user.account_type.value,
            account_status=db_user.account_status.value
        )
