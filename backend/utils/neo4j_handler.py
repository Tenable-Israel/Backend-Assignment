from neo4j import GraphDatabase
from backend.utils.config import Config

neo4j_driver = GraphDatabase.driver(Config.NEO4J_URI, auth=(Config.NEO4J_USERNAME, Config.NEO4J_PASSWORD))
