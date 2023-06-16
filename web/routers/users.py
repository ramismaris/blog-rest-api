from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from web.database.session import get_db
from web.database.models import User
from web.database.dals import UserDAL, UserTokenDAL
from web.utils.authentication import api_key_auth, generate_token

users_router = APIRouter(prefix='/user', tags=['Users'])


@users_router.get('/get/{username}')
async def get_user(
        username: str, db_session: AsyncSession = Depends(get_db), current_user: User = Depends(api_key_auth)
):
    user_from_db = await UserDAL.read(db_session, username=username)

    if len(user_from_db) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    elif current_user.is_superuser or current_user.id == user_from_db[0].id:
        return user_from_db[0]
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


class CreateUserIn(BaseModel):
    username: str
    is_superuser: bool | None = False


class CreateUserOut(BaseModel):
    username: str
    token: str


@users_router.post('/create')
async def create_user(
        body: CreateUserIn, db_session: AsyncSession = Depends(get_db), current_user: User = Depends(api_key_auth)
) -> CreateUserOut:
    if not current_user.is_superuser:
        if body.is_superuser:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    check_user = await UserDAL.read(db_session, username=body.username)
    if len(check_user) != 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='The user has already been created')

    new_user = await UserDAL.create(db_session, body.username, body.is_superuser)
    new_token = await UserTokenDAL.create(db_session, user_id=new_user.id, key=generate_token())

    return CreateUserOut(username=new_user.username, token=new_token.key)


@users_router.post('/add_token')
async def add_token(
        user_id: int, db_session: AsyncSession = Depends(get_db), current_user: User = Depends(api_key_auth)
):
    if user_id == current_user.id or current_user.is_superuser:
        check_user = await UserDAL.read(db_session, id=user_id)
        if not check_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        new_key = await UserTokenDAL.create(db_session, user_id, generate_token())
        return {
            'user_id': new_key.user_id,
            'token': new_key.key
        }
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
