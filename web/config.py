import logging
import os

from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO, format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
)

load_dotenv()

DATABASE_USER = os.getenv('POSTGRES_USER')
DATABASE_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DATABASE_HOST = os.getenv('DBHOST')
DATABASE_NAME = os.getenv('POSTGRES_DB')
DATABASE_PORT = os.getenv('POSTGRES_PORT')
DATABASE_URL = (
    f'postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
)

DB_USER_TEST = os.getenv('DB_USER_TEST')
DB_PASS_TEST = os.getenv('DB_PASS_TEST')
DB_HOST_TEST = os.getenv('DB_HOST_TEST')
DB_PORT_TEST = os.getenv('DB_PORT_TEST')
DB_NAME_TEST = os.getenv('DB_NAME_TEST')
DATABASE_URL_TEST = (
    f'postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}'
)
