from backend.utils import crud

TEST_NODE = {"attr": {"test_data": "test"},
             "label": "test_label"}
TEST_NODE_2 = {"attr": {"test_data": "test2"},
               "label": "test_label2"}


def test_create_node(delete_db):
    new_node = crud.create_node(label=TEST_NODE["label"], node_attributes=TEST_NODE["attr"])
    assert new_node.labels[0] == TEST_NODE["label"]
    assert new_node.properties == TEST_NODE["attr"]


def test_get_node_by_id(delete_db):
    new_node = crud.create_node(label=TEST_NODE["label"], node_attributes=TEST_NODE["attr"])
    ret_node = crud.get_node_by_id(new_node.node_id)
    assert ret_node.labels[0] == TEST_NODE["label"]
    assert ret_node.properties == TEST_NODE["attr"]


def test_get_nodes_by_property_and_labels(delete_db):
    crud.create_node(label=TEST_NODE["label"], node_attributes=TEST_NODE["attr"])
    res_node = crud.get_nodes_by_property_and_labels(TEST_NODE["label"], "test_data", "test")
    assert res_node[0].labels[0] == TEST_NODE["label"]
    assert res_node[0].properties == TEST_NODE["attr"]


def test_update_node(delete_db):
    new_node = crud.create_node(label=TEST_NODE["label"], node_attributes=TEST_NODE["attr"])
    new_node.properties["test_data"] = "update"
    res_node = crud.update_node(new_node.node_id, new_node.properties)
    assert TEST_NODE["label"] == res_node.labels[0]
    assert res_node.properties == {"test_data": "update"}


def test_delete_and_detach_node(delete_db):
    new_node = crud.create_node(label=TEST_NODE["label"], node_attributes=TEST_NODE["attr"])
    crud.delete_and_detach_node(new_node.node_id)
    ret_node = crud.get_node_by_id(new_node.node_id)
    assert not ret_node


def test_read_relationship(delete_db):
    new_node_1 = crud.create_node(label=TEST_NODE["label"], node_attributes=TEST_NODE["attr"])
    new_node_2 = crud.create_node(label=TEST_NODE_2["label"], node_attributes=TEST_NODE_2["attr"])
    relation_id = crud.create_relationship(new_node_1.node_id, new_node_2.node_id, "TEST")
    res_relation_id = crud.read_relationship(new_node_1.node_id, "TEST", new_node_2.node_id)
    assert relation_id == res_relation_id
