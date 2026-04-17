import strawberry
from social_media_app.schemas import User as UserModel
from typing import Optional, List, Iterable
from datetime import datetime
from strawberry import relay
from sqlalchemy.orm import Session

@strawberry.type
class UserNode(relay.Node):
    id: relay.NodeID[int]
    name: str
    email: str|None
    username: str
    account_type: str
    account_status: str

    @classmethod
    def resolve_nodes(
        cls, *, info: strawberry.Info, node_ids: Iterable[str], required: bool = False
    ) -> List["UserNode"]:
        # This method is called when refetching via the 'node' query
        # Strawberry automatically decodes the Base64 IDs back to 'int' node_ids
        results = []
        for nid in node_ids:
            data = UserNode.get(info, int(nid))
            if data:
                results.append(UserNode.from_db(info, data))
        return results
    
    @staticmethod
    def get(info: strawberry.Info, id):
        db=info.context.db
        db_user=db.query(UserModel).filter(UserModel.id==id).first()
        if db_user:
            return db_user

    @staticmethod
    def from_db(info: strawberry.Info, db_user:UserModel)->"UserNode":
        return UserNode(id=db_user.id, 
            name=db_user.firstname, 
            email=db_user.email_address, 
            username=db_user.username,
            account_type=db_user.account_type.value,
            account_status=db_user.account_status.value
        )