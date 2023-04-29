import os


class Config:
    NEO4J_URI = os.environ.get('NEO4J_URI', 'bolt://neo4j:7687')
    NEO4J_USERNAME = os.environ.get('NEO4J_USERNAME', 'neo4j')
    NEO4J_PASSWORD = os.environ.get('NEO4J_PASSWORD', 'password')
