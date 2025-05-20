# RAG Application Template 

This application template showcases the RAG scenario and aims at creating a pipeline based on LangChain framework to support dialog around predefined set of documents. For this purpose it contains the routines and elements for storing the relevant data in the vector storage and exploring LLMs for text generaton and text embedding.

## Implementation Details

The implementation uses the functionality of the platform for its basic tasks. Specifically,

- LLM serving functionality for text generation and text embedding
- Natively supported PG Vector databases for embeddings
- Python Serverless for exposing the final application as API

### Exposing LLM

To expose LLM in this scenario we use ``huggingfaceserve`` runtime. The runtime relies on the VLLM server and supports any model compatible with VLLM runtime. Please note that this runtime does not support adapters so in that case use ``kubeai`` runtime. 

To expose the text generation LLM it is necessary to specify 

- reference to the model (path). In case the model is published on HuggingFace, use ``huggingface://`` or ``hf://`` prefix. Otherwise the model may be served from S3 with ``s3://`` prefix.
- resource profile to use as GPU is needed (profile). Depends on the platform configuration.
- if HuggingFace model requires token-based authentication, path the ``HF_TOKEN`` as environment variable or as project secret reference (recommended).

To expose the text embedding model, it is necessary to specify the task as ``text_embedding``.

See [here](./howto/models.md) for further details.

### Using the vector database

In this scenario we use PGVector extension for storing the embedding. Otherwise any LangChain-compatible vector storage would work. The default database (digitalhub) of the platform already have the extension enabled so no further configuration needed. To use it, it is sufficient to provide the DB URL comprising the username and password as env variable or as project secret reference (recommended).

See [here](./howto/store_embeddings.md) for further details.

### Exposing application API

To create the RAG orchestration we use the LangChain framework and embed it into the Serverless python component to expose the API. The application refers to the LLM services and uses vector storage for retrieval.


See [here](./howto/app.md) for further details.
