
import time
from pinecone import Pinecone, SchemaBuilder
import logging
logger = logging.getLogger(__name__)
def get_index(vectordb_client: Pinecone, dimension: int, metric: str, index_name: str ):

    if not vectordb_client.indexes.exists(name=index_name):
        schema = (
            SchemaBuilder()
            .add_dense_vector_field(name="embedding", dimension=dimension, metric=metric)
            .add_sparse_vector_field(name="sparse_value")
            .build()
        )
        vectordb_client.indexes.create(name=index_name, schema=schema)
        logger.info("Index created successfully")
    else:
        logger.info("Index already exists")

    while not vectordb_client.indexes.describe(name=index_name).status.ready:
        time.sleep(2)
    pinecone_index = vectordb_client.Index(name=index_name)

    return pinecone_index