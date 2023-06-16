from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from web.database.models import User, Article, Comment, UserToken


class UserDAL:
    @staticmethod
    async def create(db_session: AsyncSession, username: str, is_superuser: bool) -> User:
        new_user = User(username=username, is_superuser=is_superuser)
        db_session.add(new_user)
        await db_session.commit()

        return new_user

    @staticmethod
    async def read(db_session: AsyncSession, **kwargs) -> User | list[User]:
        stmt = select(User).filter_by(**kwargs)
        users = await db_session.scalars(stmt)

        return users.fetchall()


class ArticleDAL:
    @staticmethod
    async def create(db_session: AsyncSession, title: str, text: str, user_id: int) -> Article:
        new_article = Article(title=title, text=text, user_id=user_id)
        db_session.add(new_article)
        await db_session.commit()

        return new_article

    @staticmethod
    async def read(db_session: AsyncSession, **kwargs) -> list[Article]:
        stmt = select(Article).filter_by(**kwargs)
        articles = await db_session.scalars(stmt)

        return articles.fetchall()

    @staticmethod
    async def update(db_session: AsyncSession, article_id: int, **kwargs) -> Article | None:
        result = await db_session.execute(
            update(Article).where(Article.id == article_id).values(kwargs).returning(Article)
        )
        await db_session.commit()

        return result.scalar_one_or_none()


class CommentDAL:
    @staticmethod
    async def create(db_session: AsyncSession, article_id: int, text: str) -> Comment:
        new_comment = Comment(article_id=article_id, text=text)
        db_session.add(new_comment)
        await db_session.commit()

        return new_comment

    @staticmethod
    async def read(db_session: AsyncSession, **kwargs) -> list[Comment]:
        stmt = select(Comment).filter_by(**kwargs)
        comments = await db_session.scalars(stmt)

        return comments.fetchall()


class UserTokenDAL:
    @staticmethod
    async def create(db_session: AsyncSession, user_id: int, key: str) -> UserToken:
        new_token = UserToken(key=key, user_id=user_id)
        db_session.add(new_token)
        await db_session.commit()

        return new_token

    @staticmethod
    async def read(db_session: AsyncSession, **kwargs) -> list[UserToken]:
        stmt = select(UserToken).filter_by(**kwargs)
        tokens = await db_session.scalars(stmt)

        return tokens.fetchall()
