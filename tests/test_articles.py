import os

from conftest import client, async_session
from web.database.dals import UserDAL, UserTokenDAL, ArticleDAL

PATH_TO_FILE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/tests/mini_backup.sql'


async def test_add_superuser():
    async with async_session() as session:
        created_user = await UserDAL.create(session, username='superadmin', is_superuser=True)
        await UserTokenDAL.create(session, created_user.id, 'test_key')

        await ArticleDAL.create(session, title='Moscow', text='Tokyo', user_id=created_user.id)
        await ArticleDAL.create(session, title='Tokyo', text='Moscow', user_id=created_user.id)


def test_all_articles():
    response = client.get("article/getAll")

    assert response.status_code == 200
    assert len(response.json()['articles']) == 2


async def test_create_article():
    async with async_session() as session:
        created_user = await UserDAL.read(session, username='superadmin')
    headers = {'Authorization': 'Bearer test_key'}
    data = {
        'title': 'Kazan',
        'text': 'Kazan - city'
    }
    response = client.post("article/create", headers=headers, json=data)

    assert response.status_code == 200
    assert response.json()['user_id'] == created_user[0].id


async def test_update_article():
    async with async_session() as session:
        before_article = await ArticleDAL.read(session, title='Kazan')
    headers = {'Authorization': 'Bearer test_key'}
    data = {
        'title': 'Moscow',
        'text': 'Moscow - city'
    }
    response = client.patch(f"article/update?article_id={before_article[0].id}", headers=headers, json=data)

    async with async_session() as session:
        after_article = await ArticleDAL.read(session, id=before_article[0].id)

    assert response.status_code == 200
    assert response.json()["updated"] == True
    assert after_article[0].title == 'Moscow'
    assert after_article[0].text == 'Moscow - city'


async def test_remove_article():
    async with async_session() as session:
        before_article = await ArticleDAL.read(session, title='Moscow')

    headers = {'Authorization': 'Bearer test_key'}
    response = client.delete(f"article/delete?article_id={before_article[0].id}", headers=headers)

    async with async_session() as session:
        after_article = await ArticleDAL.read(session, id=before_article[0].id)

    assert response.json()['deleted'] == True
    assert after_article[0].is_archived == True
