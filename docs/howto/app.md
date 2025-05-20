# Create RAG application API
Once the components and data is in place we can create a LangChain-based application and expose it as API in the platform. This will use the chat model service, the vector database, and the serverless functionality.

We create and deploy the serverless function that interacts with LLM and uses the vector store for retrieval. It uses a simple LangChaing graph composed out of two steps: retrieval and generation. The result of the generation is returned by the API.

The code of the function can be found in ``src/serve.py``. The code performs the following:

- create a LangChain pipeline that is composed of retrieval and generation steps
- relies on a predefined prompt for interacting with LLM
- uses vector storage to retrieve relevant chunks of data to add to the context
- receiving the textual query interacts with the composed pipeline to retrieve the answer

The function is then delivered as a REST API based on the Python serverless runtime.

```python
serve_func = project.new_function(
    name="rag_service", 
    kind="python", 
    python_version="PYTHON3_10", 
    code_src="src/serve.py",     
    handler="serve",
    init_function="init",
    requirements=["transformers==4.50.3", "psycopg_binary", "langchain-text-splitters", "langchain-community", "langgraph", "langchain-core", "langchain-huggingface", "langchain_postgres", "langchain[openai]"]
)

serve_run = serve_func.run(
    action="serve",
    envs=[
            {"name": "EMBEDDING_SERVICE_URL", "value": embedding_service_url},
            {"name": "CHAT_SERVICE_URL", "value": chat_service_url}
         ],
    secrets=["PG_CONN_URL"]
)
```

To test our API we make a call to the service endpoint providing a JSON with the example question:

```python
import requests

serve_service_url = serve_run.refresh().status.to_dict()["service"]["url"]

res = requests.post(f"http://{serve_service_url}",json={"question": "What is decomposition in LLM?"})
res.json()
```
