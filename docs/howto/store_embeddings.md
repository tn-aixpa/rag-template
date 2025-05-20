# Store text embeddings in vector database

We use PG Vector for storing the data into the vector database. In a provided example the document to store is taken from the Web page URL and the corresponding LangChain loader is used for this purposes. 

To accomplish the task it is necessary to perform the following steps.

1. Initialize the project to scope the functionality of the app and the corresponding services.

```python
import digitalhub as dh
project = dh.get_or_create_project("rag-demo")
```

2. Prepare the relevant secrets that should be used by the components. Specifically, for the project to work two secrets are needed:
   
- ``HF_TOKEN``: to contain the HuggingFace token if a protected model should be downloaded from the HuggingFace
- ``PG_CONN_URL``: full PGVector DB URL (with username/password) to connect to the corresponding vector store. The value may be obtained from the platform configuration or a new DB may be created from KRM with the necessary extensions.

```python
secret = project.new_secret("HF_TOKEN", secret_value="<your value>")
pg_secret = project.new_secret("PG_CONN_URL", secret_value="<full-pg-connection-url>")
```

3. Process the relevant information and store embeddings in the Vector storage

n the RAG scenario a typical task is to store the supporting information into the Vector storage and use it later for the text generation. For this purpose, consider an example scenario, where the relevant information is first scrapped from a Web page URL and then stored into the platform using the provided PGVector storage. Two components are required:
- Embeddings processor that uses Open Inference Protocol of the Embedding model service:
  ```python
    hf_embeddings = HuggingFaceInferenceAPIEmbeddings(
        api_key="ignore",
        api_url=f"http://{os.environ["EMBEDDING_SERVICE_URL"]}/v1/models/embmodel:predict"
    )
    class CEmbeddings(HuggingFaceInferenceAPIEmbeddings):
        def embed_documents(self, docs):
            return hf_embeddings.embed_documents(docs)["predictions"]

    custom_embeddings = CEmbeddings(api_key="ignore")
  ```
- PGVector storage from the platform:
  ```python
    vector_store = PGVector(
        embeddings=custom_embeddings,
        collection_name="my_docs",
        connection=os.environ["PG_CONN_URL"],
    )
  ```

See the ``src/embedding.py`` Python Job to obtain the document, create chunks, and store their embeddings using the storage.


```python
data_func = project.new_function("create_embeddings", 
                                   kind="python", 
                                   python_version="PYTHON3_10",
                                   code_src="src/embedding.py",
                                   handler="embed",
                                   requirements=["transformers==4.50.3", "psycopg_binary", "langchain-text-splitters", "langchain-community", "langgraph", "langchain-core", "langchain-huggingface", "langchain_postgres", "langchain[openai]"]
                                  )
```

```python
data_run = data_func.run(action="job", 
                         parameters={"url": "https://lilianweng.github.io/posts/2023-06-23-agent/"},
                         envs=[{"name": "EMBEDDING_SERVICE_URL", "value": embedding_service_url}],
                         secrets=["PG_CONN_URL"]
                        )
```

The results of the elaboration are stored in the corresponding database.

