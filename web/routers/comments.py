from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from web.database.dals import CommentDAL, ArticleDAL
from web.database.session import get_db
from datetime import datetime

comments_router = APIRouter(prefix='/comment', tags=['Comment'])


class CommentIn(BaseModel):
    article_id: int
    text: str


class CommentOut(BaseModel):
    comment_id: int
    article_id: int
    text: str
    created_at: datetime


@comments_router.post('/create')
async def create_comment(body: CommentIn, db_session: AsyncSession = Depends(get_db)) -> CommentOut:
    article = await ArticleDAL.read(db_session, id=body.article_id)
    if len(article) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    new_comment = await CommentDAL.create(db_session, body.article_id, body.text)

    return CommentOut(
        comment_id=new_comment.id, article_id=new_comment.article_id,
        text=new_comment.text, created_at=new_comment.created_at
    )
