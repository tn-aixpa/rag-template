# Deploy supporting LLM models

In the scenario of the RAG application two types of models are required: for text generation and for text embeddings.

1. Deploy the supporting LLM for text generation

Here we use the ``huggingfaceserve`` runtime for deploying the LLM service. Specifically, we deploy LLama3-8b-instruct model, but any HuggingFace-compatible model should work here. Alternatively, ``kubeai`` deployment may be used.

```python
chat_func = project.new_function("chat",
                                    kind="huggingfaceserve",
                                    model_name="chatmodel",
                                    path="huggingface://meta-llama/meta-llama-3-8b-instruct")
```

We run the function passing the specific execution properties:
- ``profile``: execution profile for the node selection and resource usage (depends on the platform). In this example 1xa100 refers to 1 GPU of type A100.
- ``max_length``: length of the context window for the text generation.
- ``secrets``: list of secreets to pass to LLM. Needed if, e.g., HuggingFace token is used.

```python
chat_run = chat_func.run(action="serve",
                           profile="1xa100",
                           max_length="5000",
                           secrets=["HF_TOKEN"],
                           wait=True)
```

Obtain the URL of the deployed service:

```python
chat_service_url = chat_run.refresh().status.to_dict()["service"]["url"]
```

2. Deploy the supporting LLM for embeddings

Embedding models map discrete data, such as words, to numerical vectors, which are more convenient for analysis, yet can still represent relationships between objects.    
Here we use the ``huggingfaceserve`` runtime for deploying the embedding model service. Specifically, we deploy thenlper/gte-base, but any HuggingFace-compatible model should work here. 

```python
emb_func = project.new_function("emb",
                                kind="huggingfaceserve",
                                model_name="embmodel",
                                path="huggingface://thenlper/gte-base")
```

```python
emb_run = emb_func.run(action="serve",
                       huggingface_task="text_embedding",
                       wait=True)
```

Obtain the URL of the deployed service:

```python
embedding_service_url = emb_run.refresh().status.to_dict()["service"]["url"]
```

