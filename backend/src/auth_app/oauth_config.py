# app/auth/oauth_config.py
from authlib.integrations.starlette_client import OAuth
from src.logger import get_logger
logger = get_logger(__name__)
from starlette.config import Config

# Initialize empty Config. It defaults to looking into os.environ automatically!
starlette_config = Config()

# Pass this wrapper directly to Authlib
oauth = OAuth(config=starlette_config)

# Register Google OpenID Connect configuration
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)
