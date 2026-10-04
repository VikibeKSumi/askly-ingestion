# askly-ingestion


## Part of the Askly system

| Repo | Role |
|---|---|
| [askly-data-preparation](https://github.com/VikibeKSumi/askly-data-preparation) | Raw docs → clean JSON (ETL) |
| **askly-ingestion** (this repo) | Clean JSON → chunks → embeddings → Pinecone |
| [askly](https://github.com/VikibeKSumi/askly) | RAG app: query → answer |

**Input:** clean JSON at `s3://askly-bucket/clean/`, produced by
[askly-data-preparation](https://github.com/VikibeKSumi/askly-data-preparation).
**Output:** records in Pinecone index `askly-index`, namespace `askly-namespace`
(fields: `text`, `embedding` (1024-d), `sparse_value`, metadata), read by
[askly](https://github.com/VikibeKSumi/askly).


## Configuration
Settings are in [`config/config.yaml`](config/config.yaml)
```yaml
cloud: # aws
  bucket_name: "askly-bucket"   # S3 bucket holding the documents
  clean_prefix: "clean/"        # output: cleaned JSON documents

embedding:
  dense_model_name: "llama-text-embed-v2"   
  sparse_model_name: "pinecone-sparse-english-v0" 
  dimension: 1024
  metric: "cosine"

vector_db: #pinecone
  namespace: "askly-namespace"
  index_name: "askly-index"
  batch_size: 96
```