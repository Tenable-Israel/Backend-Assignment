from fastapi import APIRouter, HTTPException, status

from backend.utils.api_utils import is_hobby_exist_by_name, is_hobby_exist_by_id
from backend.utils.schemas import Hobby, RequestHobby
from backend.utils import crud

router = APIRouter(
    prefix="/hobbies",
    tags=["hobbies"])


@router.post("/", response_model=Hobby)
async def create(hobby: RequestHobby):
    """
    Create a hobby and return the hobby and its id
    :param hobby: RequestHobby
    :return: Hobby
    """
    if is_hobby_exist_by_name(hobby.name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="A hobby with the same hobby name already exist")
    new_hobby_node = crud.create_node("Hobby", hobby.dict())
    return Hobby(**new_hobby_node.properties, id=new_hobby_node.node_id)


@router.patch("/{hobby_id:int}", response_model=Hobby)
async def update(hobby_id: int, hobby: RequestHobby):
    """
    Update the hobby based on the hobby_id
    :param hobby_id:int the hobby id
    :param hobby: RequestHobby
    :return: the updated Hobby
    """
    if not is_hobby_exist_by_id(hobby_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no hobby with this hobby ID")
    updated_hobby_node = crud.update_node(hobby_id, hobby.dict())
    return Hobby(**updated_hobby_node.properties, id=updated_hobby_node.node_id)


@router.get("/{hobby_id:int}", response_model=Hobby)
async def get(hobby_id: int):
    """
    Return the Hobby info based on the hobby id
    :param hobby_id: int
    :return: Hobby
    """
    hobby_node = crud.get_node_by_id(hobby_id)
    if not hobby_node:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no hobby with this hobby ID")
    if "Hobby" not in hobby_node.labels:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The id that was given is not of a hobby")
    return Hobby(**hobby_node.properties, id=hobby_node.node_id)


@router.delete("/{hobby_id:int}")
async def delete(hobby_id: int):
    """
    Delete and detach a hobby based on id
    :param hobby_id: int
    :return:
    """
    if not is_hobby_exist_by_id(hobby_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no hobby with this hobby ID")
    crud.delete_and_detach_node(hobby_id)
    return
