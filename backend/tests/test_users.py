from fastapi.testclient import TestClient

from backend.utils import crud
from backend.utils.schemas import User, Hobby
from backend.main import app
from backend.tests import cyphers_consts

client = TestClient(app)


def test_get_user(clean_test):
    response = client.get(f"/users/{cyphers_consts.TEST_USER_1.id}")
    assert response.status_code == 200
    assert User(**response.json()) == cyphers_consts.TEST_USER_1


def test_get_hobby():
    response = client.get(f"/hobbies/{cyphers_consts.TEST_HOBBY_1.id}")
    assert response.status_code == 200
    assert Hobby(**response.json()) == cyphers_consts.TEST_HOBBY_1


def test_get_invalid_user():
    response = client.get(f"/users/abc")
    assert response.status_code != 200


def test_create_user():
    response = client.post("/users/", data=cyphers_consts.TEST_USER_5_REQUEST.json())
    assert response.status_code == 200
    assert User(**response.json()) == cyphers_consts.TEST_USER_5


def test_create_hobby():
    response = client.post("/hobbies/", data=cyphers_consts.TEST_HOBBY_4_REQUEST.json())
    assert response.status_code == 200
    assert Hobby(**response.json()) == cyphers_consts.TEST_HOBBY_4


def test_delete_user():
    response = client.delete(f"/users/{cyphers_consts.TEST_USER_5.id}")
    assert response.status_code == 200
    assert not crud.get_node_by_id(cyphers_consts.TEST_USER_5.id)


def test_get_recommendations():
    expected_recommended_users = [cyphers_consts.TEST_USER_2, cyphers_consts.TEST_USER_3]
    response = client.get(f"/users/recommendation/{cyphers_consts.TEST_USER_1.id}")
    assert response.status_code == 200
    recommended_users = [User(**user) for user in response.json()]
    assert expected_recommended_users == recommended_users


def test_create_interest():
    response = client.put(f"/users/interest_hobby/{cyphers_consts.TEST_USER_2.id}",
                          params={"hobby_id": cyphers_consts.TEST_HOBBY_3.id})
    assert response.status_code == 200
