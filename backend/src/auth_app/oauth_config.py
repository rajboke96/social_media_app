# app/auth/oauth_config.py
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

# Load variables directly from the environment file
config = Config("auth_app/.env")
print("oauth config------->", config.get("GOOGLE_CLIENT_ID"))
oauth = OAuth(config)

# Register Google OpenID Connect configuration
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)
