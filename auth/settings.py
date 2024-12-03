import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')

ASYNC_DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

TEST_DB_PORT = os.environ.get('TEST_DB_PORT')

ASYNC_TEST_DB_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{TEST_DB_PORT}/{DB_NAME}'
TEST_DB_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{TEST_DB_PORT}/{DB_NAME}'

ACCESS_TOKEN_EXPIRATION_TIMEDELTA = os.environ.get('ACCESS_TOKEN_EXPIRATION_TIMEDELTA', 60 * 60)  # seconds
REFRESH_TOKEN_EXPIRATION_TIMEDELTA = os.environ.get('REFRESH_TOKEN_EXPIRATION_TIMEDELTA', 60*60*24)  # seconds
