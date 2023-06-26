from starlette.config import Config

config = Config(".env")
DB_URI = "postgres://avnadmin"
LOGGER_FOLDER = config("LOGGER_FOLDER", cast=str, default="src/logs/")
DATABASE_LOCAL = True
POSTGRES_DATABASE_URL = 'postgresql+psycopg2://ravi:ravi12304@postgres.ci97v9vjjjf2.eu-central-1.rds.amazonaws.com:5432/postgres'  # noqa: E501
SQLALCHEMY_DATABASE_URL = "sqlite:///endpoints.db"
