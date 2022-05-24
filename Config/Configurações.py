import os
from starlette.config import Config

# Config will be read from environment variables and/or ".env" files.
__config = Config(".env")

DOCKER_IP = os.getenv("DOCKER_IP") if os.getenv("DOCKER_IP") != None else __config('DOCKER_IP', cast=str, default="localhost")
DOCKER_PORT = os.getenv("DOCKER_PORT") if os.getenv("DOCKER_PORT") != None else __config('DOCKER_PORT', cast=str, default="2375")