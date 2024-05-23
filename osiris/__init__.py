import os
from dotenv import load_dotenv
from osiris.core.config import Settings

# load .env file
load_dotenv(os.environ.get("ENV_FILE"))

settings = Settings()
