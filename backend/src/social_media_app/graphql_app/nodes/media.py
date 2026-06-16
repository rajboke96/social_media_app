import strawberry
from .user import UserNode
from datetime import datetime
from social_media_app.schemas import Visibility, Media
from strawberry import relay
from typing import Iterable, List
from sqlalchemy import select

@strawberry.type
class MediaNode(relay.Node):
    id: relay.NodeID[int]
    name: str
    public_image_url: str

    @classmethod
    async def resolve_nodes(
        cls, *, info: strawberry.Info, node_ids: Iterable[str], required: bool = False
    ) -> List["MediaNode"]:
        # This method is called when refetching via the 'node' query
        # Strawberry automatically decodes the Base64 IDs back to 'int' node_ids
        results = []
        for nid in node_ids:
            data = await MediaNode.get(info, int(nid))
            if data:
                results.append(MediaNode.from_db(info, data))
        return results

    @staticmethod
    async def get(info: strawberry.Info, id):
        db_factory=info.context.db_factory
        async with db_factory() as db:
            statement=select(Media).where(Media.id==id)
            result=await db.execute(statement)
            db_user=result.scalar_one_or_none()
            return db_user
    
    @staticmethod
    async def from_db(info: strawberry.Info, db_user:Media)->"MediaNode":
        return MediaNode(id=db_user.id,
            name=db_user.name,
            public_image_url=db_user.public_image_url
        )