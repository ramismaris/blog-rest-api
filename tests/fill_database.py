import os

from sqlalchemy import create_engine
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()

DATABASE_USER = os.getenv('POSTGRES_USER')
DATABASE_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DATABASE_HOST = 'localhost'
DATABASE_NAME = os.getenv('POSTGRES_DB')
DATABASE_PORT = os.getenv('POSTGRES_PORT')
DATABASE_URL = (
    f'postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
)

PATH_TO_FILE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/tests/mini_backup.sql'

engine = create_engine("".join(DATABASE_URL.split("+asyncpg")), echo=True)

with engine.connect() as con:
    with open(PATH_TO_FILE) as file:
        query = text(file.read())
        con.execute(query)

    con.commit()
