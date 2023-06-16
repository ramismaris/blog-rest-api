import hashlib
import time

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from web.database.dals import UserTokenDAL, UserDAL
from web.database.session import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def api_key_auth(db_session: AsyncSession = Depends(get_db), api_key: str = Depends(oauth2_scheme)):
    api_key = await UserTokenDAL.read(db_session, key=api_key)

    if len(api_key) != 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Forbidden')

    user = await UserDAL.read(db_session, id=api_key[0].user_id)

    return user[0]


def generate_token() -> str:
    time_stamp = str(time.time() * 10000000)
    new_key = str(hashlib.md5(time_stamp.encode()).hexdigest())
    return new_key
