from pinecone import Pinecone

class BuildRecords():

    def __init__(self, vectordb_client: Pinecone, batch_size: int, dense_model_name: str, sparse_model_name: str):
        self.vectordb_client = vectordb_client
        self.DENSE_MODEL_NAME = dense_model_name
        self.SPARSE_MODEL_NAME = sparse_model_name
        self.BATCH_SIZE = batch_size

    def dense_embedding(self, chunks: list[str]) -> list[list[float]]:
        dense_embeddings = []
        for i in range(0, len(chunks), self.BATCH_SIZE):
            embedding = self.vectordb_client.inference.embed(
                model=self.DENSE_MODEL_NAME,
                inputs=chunks[i: i+self.BATCH_SIZE],
                parameters={"input_type": "passage", "truncate": "END"}
            )
            dense_embeddings.extend(e["values"] for e in embedding)

        return dense_embeddings

    
    def sparse_embedding(self, chunks: list[str]) -> list[dict]:
        sparse_embeddings = []
        for i in range(0, len(chunks), self.BATCH_SIZE):
            embedding = self.vectordb_client.inference.embed(
                model=self.SPARSE_MODEL_NAME,
                inputs=chunks[i: i+self.BATCH_SIZE],
                parameters={"input_type": "passage", "truncate": "END"}
            )
            sparse_embeddings.extend({"indices": e["sparse_indices"], "values": e["sparse_values"]} for e in embedding)

        return sparse_embeddings


        