from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, constr, parse_obj_as
from typing import Optional

from web.database.models import User
from web.database.session import get_db
from web.database.dals import ArticleDAL, CommentDAL
from web.utils.authentication import api_key_auth

article_crud_router = APIRouter(prefix='/article', tags=['Articles'])


class ArticleOut(BaseModel):
    user_id: int
    title: str
    text: str

    class Config:
        orm_mode = True


class AllArticlesOut(BaseModel):
    articles: list[ArticleOut]


@article_crud_router.get('/getAll')
async def get_all_articles(db_session: AsyncSession = Depends(get_db)) -> AllArticlesOut:
    articles = await ArticleDAL.read(db_session)

    return AllArticlesOut(articles=parse_obj_as(list[ArticleOut], articles))


class ArticleWithCommentOut(BaseModel):
    article: ArticleOut
    comments: list | None


@article_crud_router.get('/get/{id}')
async def get_article(id: int, db_session: AsyncSession = Depends(get_db)) -> ArticleWithCommentOut:
    article = await ArticleDAL.read(db_session, id=id)

    if len(article) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Wrong ID')
    else:
        article = article[0]
        comments = await CommentDAL.read(db_session, id=article.id)

    return ArticleWithCommentOut(
        article=ArticleOut(user_id=article.user_id, title=article.title, text=article.text),
        comments=comments if comments else None
    )


class CreateArticleIn(BaseModel):
    title: str
    text: str


class CreateArticleOut(BaseModel):
    article_id: int

    class Config:
        orm_mode = True


@article_crud_router.post('/create')
async def create_article(
        body: CreateArticleIn, db_session: AsyncSession = Depends(get_db), user: User = Depends(api_key_auth)
) -> ArticleOut:
    new_article = await ArticleDAL.create(db_session, body.title, body.text, user.id)

    return ArticleOut(user_id=user.id, title=new_article.title, text=new_article.text)


class UpdateArticleIn(BaseModel):
    title: Optional[constr(min_length=1)]
    text: Optional[constr(min_length=1)]


@article_crud_router.patch('/update')
async def update_article(
        article_id: int,
        body: UpdateArticleIn,
        db_session: AsyncSession = Depends(get_db),
        user: User = Depends(api_key_auth)
):
    user_params_for_update = body.dict(exclude_none=True)
    article = await ArticleDAL.read(db_session, id=article_id, is_archived=False)

    if user_params_for_update == {}:
        raise HTTPException(status_code=422, detail="At least one parameter for user update info should be provided")
    if len(article) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    elif user.is_superuser or article[0].user_id == user.id:
        await ArticleDAL.update(db_session, article_id, **user_params_for_update)
        return {'updated': True}

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@article_crud_router.delete('/delete')
async def delete_article(
        article_id: int, db_session: AsyncSession = Depends(get_db), user: User = Depends(api_key_auth)
):
    article = await ArticleDAL.read(db_session, id=article_id, is_archived=False)

    if len(article) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    elif user.is_superuser or article[0].user_id == user.id:
        await ArticleDAL.update(db_session, article_id, is_archived=True)
        return {'deleted': True}

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
