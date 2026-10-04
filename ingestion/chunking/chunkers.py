from ingestion.chunking.code_blocks import protect_code, restore_code
from ingestion.chunking.sections import split_by_headers
from ingestion.chunking.blocks import split_blocks, block_to_pieces


def get_chunk(docs: list[dict]) -> tuple[list[dict], list[dict]]:


    parents, chunks = [], []
    for doc in docs:
        meta = {k: v for k, v in doc.items() if k not in ("id", "text")}
        text, code_blocks = protect_code(doc["text"])
        pos = 0       

        for si, sec in enumerate(split_by_headers(text, max_level=6)):
            pid = f"{doc['id']}#S{si}"
            parents.append({
                "id": pid,
                "text": f"{sec['section']}:\n{restore_code(sec['text'], code_blocks)}",
                "doc_id": doc["id"],
                "section": sec["section"],
            })

            for kind, block in split_blocks(sec["text"]):
                for piece in block_to_pieces(kind, block, code_blocks, sec["section"]):
                    chunks.append({
                        "id": f"{doc['id']}#{pos}",
                        "chunk_text": piece if kind == "table" else f"{sec['section']}:\n{piece}",
                        "doc_id": doc["id"],
                        "parent_id": pid,
                        "section": sec["section"],
                        "chunk_type": kind,
                        "position": pos,
                        **meta,
                    })
                    pos += 1

    return parents, chunks



if __name__ == "__main__":
    from ingestion.load_docs import load_doc_from_cloud
    import boto3
    from config.config import config
    from dotenv import load_dotenv
    load_dotenv()

    
    client = boto3.client("s3")
    BUCKET_NAME = config.BUCKET_NAME
    CLEAN_PREFIX = config.CLEAN_PREFIX

    resp = client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=CLEAN_PREFIX)
    keys = [o["Key"] for o in resp.get("Contents", []) if not o["Key"].endswith("/")]
    key = keys[0]

    doc = load_doc_from_cloud(client=client, bucket_name=BUCKET_NAME, key=key)
    parents, chunks = get_chunk(docs=[doc])
    print(len(parents))
    print(len(chunks))

    for k, v in chunks[0].items():
        print(k)
        
