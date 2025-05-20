# RAG Template Application
RAG template based on LangChain pipeline.


#### AIxPA

-   `kind`: product-template
-   `ai`: NLP
-   `domain`: PA

A simple Retrieval-Augmented Generation (RAG) application based on the platform functionality for demonstration purposes.
The template demonstrates the usage of the platform for the key RAG functionality using LangChain framework. Specifically,

- use LLM serving functionality for supporting operations (text generation and embeddings)
- create text embedding and store them in the vector database provided with the platform
- create and expose the RAG application API as a serverless function

## Usage

See the  usage documentation [here](./docs/usage.md).

## How To

- [Store information embeddings in a vector database](./docs/howto/store_embeddings.md)
- [Deploy supporting LLM models](./docs/howto/models.md)
- [Create a RAG application API](./docs/howto/app.md)
