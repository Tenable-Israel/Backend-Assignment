from fastapi import APIRouter, HTTPException, status

from backend.utils.api_utils import is_user_exist_by_username, is_user_exist_by_id
from backend.utils.crud import find_nodes_with_relations, create_relationship
from backend.utils.schemas import User, RequestUser, UserProperties
from backend.utils.neo4j_handler import neo4j_driver
from typing import List
from backend.utils import crud

router = APIRouter(
    prefix="/users",
    tags=["users"])


@router.post("/", response_model=User)
async def create_user(user: RequestUser):
    """
        Create User if the username does not exist. if exist raise HTTP_400_BAD_REQUEST
        :param user: User object according to the schema
        :return: the new User
    """
    if is_user_exist_by_username(user.name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="A user with the same username already exist")
    new_user_node = crud.create_node("User", user.dict())
    return User(**new_user_node.properties, id=new_user_node.node_id)


@router.patch("/{user_id:int}", response_model=User)
async def update_user(user_id: int, user_info: UserProperties):
    """
    Update the user info (except username)
    :param user_id: id of the user
    :param user_info: the new UserProperties
    :return: the new User
    """
    if not is_user_exist_by_id(user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no user with this user ID")
    new_user_node = crud.update_node(user_id, user_info.dict())
    return User(**new_user_node.properties, id=new_user_node.node_id)


@router.get("/{user_id:int}", response_model=User)
async def get_user(user_id):
    """
    Get user info by id, if not exist raise 404
    :param user_id: int
    :return: User
    """
    user_node = crud.get_node_by_id(user_id)
    if not user_node:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no user with this user ID")
    if "User" not in user_node.labels:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Got node_id of non-user node")
    return User(**user_node.properties, id=user_node.node_id)


@router.delete("/{user_id}")
async def delete(user_id: int):
    """
    Delete specific user
    :param user_id: the user id
    :return: msg
    """
    if not is_user_exist_by_id(user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no user with this username")
    crud.delete_and_detach_node(user_id)
    return {f"User {user_id} was deleted"}


@router.put("/interest_hobby/{user_id:int}")
async def interest_hobby(user_id: int, hobby_id: int):
    """
    Create a relation between user and hobby
    :param user_id: userid
    :param hobby_id: hobby_id
    :return: relationship_id
    """
    if not is_user_exist_by_id(user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no user with this username")
    relationship_id = create_relationship(user_id, hobby_id, "INTERESTED")
    return relationship_id


@router.delete("/disinterest_hobby/{user_id:int}")
async def disinterest_hobby(user_id: int, hobby_id: int):
    """
    Delete relationship of user and hobby
    :param user_id: (int)
    :param hobby_id: (int)
    :return:
    """
    relationship_id = crud.read_relationship(user_id, "INTERESTED", hobby_id)
    if not relationship_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There is no relationship between the user and this hobby")
    crud.delete_relationship(relationship_id)
    return


@router.get("/recommendation/{user_id}")
async def recommendation(user_id):
    """
    Get all the users that have the same interests as the given user
    :param user_id: the user id
    :return: list of users recommended to be friends
    """
    if not is_user_exist_by_id(user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no user with this username")
    data = find_nodes_with_relations(user_id, "Hobby", "INTERESTED")
    if not data:
        return {"no recommendations"}
    recommended_users = [User(**node.properties, id=node.node_id) for node in data]
    return recommended_users
