

if __name__ == "__main__":
    try:
        import boto3
        from pinecone import Pinecone
        import os
        from dotenv import load_dotenv
        load_dotenv()
        import time

        from ingestion.ingestion import AsklyIngestion
        from ingestion.upsert import UpsertRecords
        from ingestion.records import BuildRecords
        from ingestion.get_index import get_index
        from config.config import config

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
        print("Ingestion successful.")
    except Exception as e:
        print(f"{e}")