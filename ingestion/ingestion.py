from ingestion.load_docs import load_doc_from_cloud
from ingestion.chunking.chunkers import get_chunk
from ingestion.records import BuildRecords
from ingestion.upsert import UpsertRecords
import logging
logger = logging.getLogger(__name__)


class AsklyIngestion():

    def __init__(self,
            storage_client,
            bucket_name: str,
            clean_prefix: str,
            build_records: BuildRecords,
            upsert_record: UpsertRecords
        ):

        self.BUCKET_NAME = bucket_name
        self.CLEAN_PREFIX = clean_prefix
        self.build_records = build_records
        self.storage_client = storage_client
        self.upsert_record = upsert_record
        

    def run_ingestion(self):

        logger.info("Loading docs from cloud (S3)...")
        resp = self.storage_client.list_objects_v2(Bucket=self.BUCKET_NAME, Prefix=self.CLEAN_PREFIX)
        keys = [o["Key"] for o in resp.get("Contents", []) if not o["Key"].endswith("/")]
        docs = []
        for key in keys:
            doc = load_doc_from_cloud(client=self.storage_client, bucket_name=self.BUCKET_NAME, key=key)
            docs.append(doc)
        logger.info("Loaded %s docs", len(docs))

        logger.info("Preparing chunks...")
        parents, chunks = get_chunk(docs)
        logger.info("Loaded %s chunks", len(chunks))

        logger.info("Embedding chunks...")
        chunks_text = [chunk["chunk_text"] for chunk in chunks]
        dense_embeddings = self.build_records.dense_embedding(chunks=chunks_text)
        sparse_embeddings = self.build_records.sparse_embedding(chunks=chunks_text)
        logger.info("Dense and sparse embedding complete.")

        logger.info("Preparing records")
        records = [
            {
                "_id": chunk["id"],
                "text": chunk["chunk_text"],
                **{k: v for k, v in chunk.items() if k not in ("id", "chunk_text")},
                "embedding": dense,
                "sparse_value": sparse,
            }
            for chunk, dense, sparse in zip(chunks, dense_embeddings, sparse_embeddings)
        ]
        
        logger.info("Upserting to pinecone...")
        self.upsert_record.upsert(records=records)
        logger.info("Upsertion complete")