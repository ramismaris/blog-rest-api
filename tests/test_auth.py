from web.database.dals import UserDAL, UserTokenDAL
from conftest import client, async_session



def test_register():
    test_user_data = {'username': 'john_doe',}
    headers = {'Authorization': 'Bearer test_key'}
    response = client.post("/user/create", headers=headers, json=test_user_data)

    assert response.status_code == 200


def test_wrong_authorization():
    headers = {'Authorization': 'Bearer #fffff'}
    response = client.post("user/create", headers=headers)

    assert response.status_code == 401


async def test_add_token():
    headers = {'Authorization': 'Bearer test_key'}
    response = client.post("user/add_token?user_id=1", headers=headers)
    res_data = response.json()
    async with async_session() as session:
        new_token = await UserTokenDAL.read(session, key=res_data['token'])

    assert response.status_code == 200
    assert res_data['user_id'] == new_token[0].user_id
