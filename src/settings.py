from starlette.config import Config

config = Config(".env")
DB_URI = "postgres://avnadmin"
LOGGER_FOLDER = config("LOGGER_FOLDER", cast=str, default="src/logs/")
