from pydantic import BaseModel
from typing import Optional


class NodeBase(BaseModel):
    node_id: int
    labels: list


class Node(NodeBase):
    properties: Optional[dict] = None


class RequestHobby(BaseModel):
    name: str
    description: Optional[str] = None


class Hobby(RequestHobby):
    id: int


class BaseUser(BaseModel):
    name: str  # unique username


class RequestUser(BaseUser):
    first_name: str
    last_name: str
    nickname: Optional[str] = None


class UserProperties(BaseModel):
    first_name: str
    last_name: str
    nickname: Optional[str] = None


class User(RequestUser):
    id: int
