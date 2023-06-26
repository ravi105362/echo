from starlette.config import Config

config = Config(".env")
DB_URI = "postgres://avnadmin"
LOGGER_FOLDER = config("LOGGER_FOLDER", cast=str, default="src/logs/")
DATABASE_LOCAL = True
POSTGRES_DATABASE_URL = 'postgresql+psycopg2://<URL>'  # noqa: E501
SQLALCHEMY_DATABASE_URL = "sqlite:///endpoints.db"
