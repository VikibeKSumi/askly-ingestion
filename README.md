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
