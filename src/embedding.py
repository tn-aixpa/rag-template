import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector
import os
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings


def embed(url):
    service_url = os.environ["EMBEDDING_SERVICE_URL"]
    hf_embeddings = HuggingFaceInferenceAPIEmbeddings(
        api_key="ignore",
        api_url=f"http://{service_url}/v1/models/embmodel:predict"
    )
    class CEmbeddings(HuggingFaceInferenceAPIEmbeddings):
        def embed_documents(self, docs):
            return hf_embeddings.embed_documents(docs)["predictions"]

    custom_embeddings = CEmbeddings(api_key="ignore")

    vector_store = PGVector(
        embeddings=custom_embeddings,
        collection_name="my_docs",
        connection=os.environ["PG_CONN_URL"],
    )

    loader = WebBaseLoader(
        web_paths=(url,),
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                class_=("post-content", "post-title", "post-header")
            )
        ),
    )
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    all_splits = text_splitter.split_documents(docs)

    vector_store.add_documents(documents=all_splits)
