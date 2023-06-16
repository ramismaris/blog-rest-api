from fastapi import FastAPI

from web.routers.articles import article_crud_router
from web.routers.users import users_router
from web.routers.comments import comments_router

app = FastAPI()

app.include_router(article_crud_router)
app.include_router(users_router)
app.include_router(comments_router)
