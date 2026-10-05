
import boto3
from pinecone import Pinecone
import os
from dotenv import load_dotenv
load_dotenv()
import time
import logging
from rich.logging import RichHandler

from ingestion.ingestion import AsklyIngestion
from ingestion.upsert import UpsertRecords
from ingestion.records import BuildRecords
from ingestion.get_index import get_index
from config.config import config


file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
logging.basicConfig(
        level=logging.INFO,
        format="%(name)s: %(message)s", 
        handlers=[RichHandler(), file_handler]
    )
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    try:
        
        DENSE_MODEL_NAME = config.DENSE_MODEL_NAME
        SPARSE_MODEL_NAME = config.SPARSE_MODEL_NAME
        BUCKET_NAME = config.BUCKET_NAME
        CLEAN_PREFIX = config.CLEAN_PREFIX
        INDEX_NAME = config.INDEX_NAME
        BATCH_SIZE = config.BATCH_SIZE
        NAMESPACE = config.NAMESPACE
        DIMENSION = config.DIMENSION
        METRIC = config.METRIC

        storage_client = boto3.client("s3")
        pinecone_client = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

        pinecone_index = get_index(
            vectordb_client=pinecone_client,
            dimension=DIMENSION,
            metric=METRIC,
            index_name=INDEX_NAME
        )

        ingestion = AsklyIngestion(
            storage_client=storage_client,
            bucket_name=BUCKET_NAME,
            clean_prefix=CLEAN_PREFIX,
            build_records=BuildRecords(
                    vectordb_client=pinecone_client,
                    batch_size=BATCH_SIZE,
                    dense_model_name=DENSE_MODEL_NAME,
                    sparse_model_name=SPARSE_MODEL_NAME
                ),
            upsert_record=UpsertRecords(
                    index=pinecone_index,
                    namespace=NAMESPACE,
                    batch_size=BATCH_SIZE
                )
        )

        ingestion.run_ingestion()
        logger.info("Ingestion successful")
    except Exception as e:
        logger.exception(f"Ingestion failed: {e}")