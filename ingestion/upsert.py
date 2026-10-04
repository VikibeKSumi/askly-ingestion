from pinecone import Index


class UpsertRecords():

    def __init__(self, index: Index, namespace: str, batch_size: int):
        self.index = index
        self.NAMESPACE = namespace
        self.BATCH_SIZE = batch_size

    def upsert(self, records: list[dict]):
        self.index.documents.batch_upsert(
            namespace=self.NAMESPACE,
            documents=records,
            batch_size= self.BATCH_SIZE
        )

    