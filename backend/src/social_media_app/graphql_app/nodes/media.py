import strawberry
from src.logger import get_logger
logger = get_logger(__name__)

from social_media_app.schemas import Media
from strawberry import relay
from typing import Iterable, List
from sqlalchemy import select
import os
from imgproxy import ImgProxy

IMGPROXY_INTERNAL_HOST = os.environ.get("IMGPROXY_INTERNAL_HOST", "http://localhost:8080")
IMGPROXY_EXTERNAL_URL = os.environ.get("IMGPROXY_EXTERNAL_URL", "http://localhost:8080")
IMGPROXY_KEY = os.environ.get("IMGPROXY_KEY")
IMGPROXY_SALT = os.environ.get("IMGPROXY_SALT")

def generate_secure_imgproxy_url(source_uri: str, width: int, height: int, extension: str = "webp", advanced_args: list = None) -> str:
    """
    Unified signature wrapper tool. Uses the klen/imgproxy native function call 
    protocol to append advanced string modifiers cleanly before generating signatures.
    """
    # 1. Initialize the base ImgProxy object with structural options
    img_url = ImgProxy(
        source_uri,
        proxy_host=IMGPROXY_INTERNAL_HOST,
        key=IMGPROXY_KEY,
        salt=IMGPROXY_SALT,
        resizing_type="fill",
        width=width,
        height=height,
        extension=extension
    )
    
    if advanced_args:
        signed_path = img_url(*advanced_args)  # Calls __call__ method natively
    else:
        signed_path = str(img_url)             # Standard string conversion
    
    # 3. Swap out internal Docker container routing name for your client browser path
    return signed_path.replace(IMGPROXY_INTERNAL_HOST, IMGPROXY_EXTERNAL_URL)

@strawberry.type
class MediaNode(relay.Node):
    id: relay.NodeID[int]
    name: str
    # public_image_url: str

    # Dynamically build the imgproxy links on demand
    @strawberry.field
    def url(self, width: int = 500, height: int = 500) -> str:
        # Match your local container shared directory syntax schema
        local_source_uri = f"local://root/{self.name}"
        
        # Execute your working signing factory function
        return generate_secure_imgproxy_url(local_source_uri, width, height)

    @strawberry.field
    def feed_url(self, width: int = 600, height: int = 450) -> str:
        """Main Feed View: Standard timeline layout size dimensions."""
        local_source_uri = f"local://root/{self.name}"
        return generate_secure_imgproxy_url(local_source_uri, width, height, "webp")

    @strawberry.field
    def thumbnail_url(self, width: int = 150, height: int = 150) -> str:
        """Grid Profile Thumbnails: Shrunk to a 1:1 crisp square layout."""
        local_source_uri = f"local://root/{self.name}"
        return generate_secure_imgproxy_url(local_source_uri, width, height, "webp")

    @strawberry.field
    def blur_url(self, width: int = 500, height: int = 500) -> str:
        """Progressive Blur Placeholder: Small 20x20 blurred JPEG image."""
        local_source_uri = f"local://root/{self.name}"
        
        # Pass advanced parameters as plain string arguments matching imgproxy's URL options.
        # This appends 'bl:5' and 'q:30' correctly into the signed token path matrix.
        advanced_filters = [
            "bl:5",   # Gaussian blur strength multiplier filter
            "q:30"    # Drops image processing quality down to save payload bandwidth bytes
        ]
        return generate_secure_imgproxy_url(local_source_uri, width, height, "jpg", advanced_filters)

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
        logger.info('exit')
        return results

    @staticmethod
    async def get(info: strawberry.Info, id):
        db_factory=info.context.db_factory
        async with db_factory() as db:
            statement=select(Media).where(Media.id==id)
            result=await db.execute(statement)
            db_user=result.scalar_one_or_none()
            logger.info('exit')
            return db_user
    
    @staticmethod
    async def from_db(info: strawberry.Info, db_user:Media)->"MediaNode":
        logger.info('exit')
        return MediaNode(id=db_user.id,
            name=db_user.name,
            # public_image_url=db_user.public_image_url
        )
