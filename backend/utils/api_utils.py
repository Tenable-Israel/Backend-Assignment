from backend.utils.crud import get_node_by_id, get_nodes_by_property_and_labels


def is_user_exist_by_username(username: str) -> bool:
    nodes = get_nodes_by_property_and_labels("User", "name", username)
    if nodes:
        return True
    return False


def is_user_exist_by_id(user_id: int) -> bool:
    nodes = get_node_by_id(user_id)
    if nodes and "User" in nodes.labels:
        return True
    return False


def is_hobby_exist_by_name(hobby_name: str) -> bool:
    nodes = get_nodes_by_property_and_labels("Hobby", "name", hobby_name)
    if nodes:
        return True
    return False


def is_hobby_exist_by_id(hobby_id: int) -> bool:
    nodes = get_node_by_id(hobby_id)
    if nodes and "Hobby" in nodes.labels:
        return True
    return False
