from backend.utils.schemas import Node
from typing import Optional, List
from backend.utils.neo4j_handler import neo4j_driver
from fastapi import HTTPException, status


def create_node(label: str, node_attributes: dict) -> Node:
    """
    Create  a new node and returns the node info and its id
    :param label: the node label
    :param node_attributes: node attributes
    :return: the new node
    """
    unpacked_attributes = 'SET ' + ', '.join(f'new_node.{key}=\'{value}\'' for (key, value) in node_attributes.items())
    cypher = f"""CREATE (new_node:{label}) 
             {unpacked_attributes} 
             RETURN new_node, LABELS(new_node) as labels, ID(new_node) as id"""
    data = execute_cypher(cypher)[0]

    node = Node(node_id=data['id'],
                labels=data['labels'],
                properties=data['new_node'])
    return node


def get_node_by_id(node_id: int) -> Node | None:
    """
    Get info based on its id
    :param node_id: the id of the desired node
    :return: (str)
    """
    cypher = f"""MATCH (node) 
             WHERE ID(node) = {node_id} 
             RETURN node, LABELS(node) as labels, ID(node) as id"""
    data = execute_cypher(cypher)
    if not data:
        return None
    data = data[0]
    node = Node(node_id=data['id'],
                labels=data['labels'],
                properties=data['node'])
    return node


def get_nodes_by_property_and_labels(search_node_labels: str, search_node_property: str,
                                     node_property_value: str) -> List[Node]:
    """
    Get all the nodes that matches the property = property_value
    :param search_node_labels:
    :param search_node_property:
    :param node_property_value:
    :return:
    """
    cypher = f"""MATCH (node:{search_node_labels}) 
             WHERE node.{search_node_property} = \'{node_property_value}\' 
             RETURN ID(node) as id, LABELS(node) as labels ,node"""
    data = execute_cypher(cypher)
    nodes = [Node(node_id=node['id'],
                  labels=node['labels'],
                  properties=node['node']) for node in data]
    return nodes


def update_node(node_id: int, node_attributes: dict) -> Node | None:
    """
     Update the node info by node ID
    :param node_id: the id of the desired node
    :param node_attributes: new node info
    :return: (str)
    """
    unpacked_attributes = 'SET ' + ', '.join(f'node.{key}=\'{value}\'' for (key, value) in node_attributes.items())
    cypher = f"""MATCH (node) 
             WHERE ID(node) = {node_id} 
             {unpacked_attributes} 
             RETURN node, ID(node) as id, LABELS(node) as labels"""
    data = execute_cypher(cypher)
    if not data:
        return None
    data = data[0]
    node = Node(node_id=data['id'],
                labels=data['labels'],
                properties=data['node'])
    return node


def delete_and_detach_node(node_id: int):
    """
    Create a cypher for delete and detach node
    :param node_id:
    :return: (str)
    """
    cypher = f"""MATCH (node) 
             WHERE ID(node) = {node_id} 
             DETACH DELETE node"""
    execute_cypher(cypher)
    return


def create_relationship(source_node_id: int, target_node_id: int, relationship_type: str,
                        relationship_attributes: Optional[dict] = None) -> int | None:
    """
    Create a cypher that will create a relationship between two nodes
    first it wil find the nodes based on their id
    create the relationship (source)->(target) and return relationship_id
    :param source_node_id: the source node id (exp: User)
    :param target_node_id: the target node id (exp: Hobby)
    :param relationship_type: (str) the relationship type
    :param relationship_attributes: optional relationship attribute
    :return: relationship id
    """
    if relationship_attributes:
        unpacked_attributes = 'SET ' + ', '.join(
            f'relationship.{key}=\'{value}\'' for (key, value) in relationship_attributes.items())
    else:
        unpacked_attributes = ''

    cypher = f"""
           MATCH (source) WHERE ID(source) = {source_node_id}
           MATCH (target) WHERE ID(target) = {target_node_id}
           CREATE (source)-[relationship:{relationship_type}]->(target)
           {unpacked_attributes}
           RETURN ID(relationship) as id
           """
    data = execute_cypher(cypher)
    if not data:
        return None
    data = data[0]
    return data["id"]


def delete_relationship(relationship_id: int):
    """
    Create a cypher that will delete the relationship based on the id
    :param relationship_id: (int)
    :return:
    """
    cypher = f"""
            MATCH (a)-[relationship]->(b)
            WHERE ID(relationship) = {relationship_id}
            DELETE relationship
            """
    execute_cypher(cypher)
    return


def find_nodes_with_relations(source_node_id: int, target_label: str, relationship_type: str) -> List[Node] | None:
    """
    Create a cypher that will return a list of related node id
    :param source_node_id: the node id
    :param target_label: (str) the label of the desired target node (exp: Hobby)
    :param relationship_type: (str) the label of the desired relationship (exp: INTERESTED)
    :return: the List[Node] of the related node
    """
    cypher = f"""MATCH (node WHERE ID(node) = {source_node_id}) - [{relationship_type}] -> (target:{target_label}) 
                        WITH node, collect(target) as targets, labels(node) as source_label
                        UNWIND targets as t 
                        MATCH (s WHERE id(s) <> id(node))- [{relationship_type}]->(t) 
                        WHERE labels(s) = source_label
                        RETURN DISTINCT s as node, ID(s) as id, LABELS(s) as labels"""

    result = execute_cypher(cypher)
    nodes_list = [Node(node_id=node['id'],
                       labels=node['labels'],
                       properties=node['node']) for node in result]
    if not result:
        return None
    return nodes_list


def read_relationship(source_node_id: int, relationship_type: str, target_node_id: int) -> int | None:
    """
    Get the relationship id of the relation between (source) -[relationship_type] -> (target)
    None if does not exist
    :param source_node_id: int (exp: User.id)
    :param relationship_type: (str) (exp: INTERESTED)
    :param target_node_id: int (exp: Hobby.id)
    :return: (int) relationship id
    """
    cypher = f"""MATCH (node WHERE ID(node) = {source_node_id}) - [r: {relationship_type}] -> 
    (target WHERE ID(target) = {target_node_id})
                RETURN ID(r) as rid"""
    result = execute_cypher(cypher)
    if not result:
        return None
    return result[0]["rid"]


def execute_cypher(cypher):
    """
    Execute a cypher query and return the result
    :param cypher: str
    :return: result
    """
    try:
        with neo4j_driver.session() as session:
            res = session.run(query=cypher)
            data = res.data()
        return data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"db driver error {e}")
