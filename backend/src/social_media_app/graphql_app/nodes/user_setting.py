import strawberry
from .user import UserNode
from social_media_app.schemas import UserSetting
from strawberry import relay
from typing import Iterable, List

@strawberry.type
class UserSettingNode(relay.Node):
    id: relay.NodeID[int]
    user: UserNode
    theme: str

    @classmethod
    def resolve_nodes(
        cls, *, info: strawberry.Info, node_ids: Iterable[str], required: bool = False
    ) -> List["UserSettingNode"]:
        # This method is called when refetching via the 'node' query
        # Strawberry automatically decodes the Base64 IDs back to 'int' node_ids
        results = []
        for nid in node_ids:
            data = UserSettingNode.get(info, int(nid))
            if data:
                results.append(UserSettingNode.from_db(data))
        return results

    @staticmethod
    def get_user_setting(info: strawberry.Info, user_id):
        db=info.context.db
        db_user_posts=db.query(UserSetting).filter(UserSetting.user_id==user_id).first()
        return db_user_posts