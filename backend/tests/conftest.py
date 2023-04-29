import pytest


from backend.utils.neo4j_handler import neo4j_driver as test_neo4j_driver
from backend.tests import cyphers_consts


@pytest.fixture()
def add_users():
    with test_neo4j_driver.session() as session:
        for node in cyphers_consts.USERS_TO_ADD:
            unpacked_attributes = 'SET ' + ', '.join(
                f'new_node.{key}=\'{value}\'' for (key, value) in node.dict().items())
            cypher = f"""CREATE (new_node:User) 
                             {unpacked_attributes} 
                             RETURN new_node, LABELS(new_node) as labels, ID(new_node) as id"""
            session.run(query=cypher)


@pytest.fixture()
def add_hobbies():
    with test_neo4j_driver.session() as session:
        for node in cyphers_consts.HOBBIES_TO_ADD:
            unpacked_attributes = 'SET ' + ', '.join(
                f'new_node.{key}=\'{value}\'' for (key, value) in node.dict().items())
            cypher = f"""CREATE (new_node:Hobby) 
                         {unpacked_attributes} 
                         RETURN new_node, LABELS(new_node) as labels, ID(new_node) as id"""
            session.run(query=cypher)


@pytest.fixture()
def add_user_hobby_relations():
    with test_neo4j_driver.session() as session:
        for relation in cyphers_consts.RELATIONS_TO_ADD:
            source_node_id = relation[0]
            target_node_id = relation[1]
            cypher = f"""
               MATCH (source) WHERE ID(source) = {source_node_id}
               MATCH (target) WHERE ID(target) = {target_node_id}
               CREATE (source)-[relationship:INTERESTED]->(target)
               RETURN ID(relationship) as id"""
            session.run(query=cypher)


@pytest.fixture()
def populate_db(add_users, add_hobbies, add_user_hobby_relations):
    return


@pytest.fixture()
def delete_db():
    delete_all = "MATCH (n) DETACH DELETE n"
    with test_neo4j_driver.session() as session:
        session.run(query=delete_all)


@pytest.fixture()
def clean_test(delete_db, populate_db):
    return
