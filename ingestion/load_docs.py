from botocore.client import BaseClient
import json

def load_doc_from_cloud(client: BaseClient, bucket_name: str, key: str) -> dict:

    obj = client.get_object(
        Bucket=bucket_name,
        Key=key
    )
    raw = obj["Body"].read().decode("utf-8")

    return json.loads(raw)


if __name__ == "__main__":
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
    doc = load_doc_from_cloud(client=boto3.client('s3'), bucket_name=BUCKET_NAME, key=key)
    print(type(doc))