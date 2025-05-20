import bs4
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector
import os
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings

from langchain import hub
from langchain_core.documents import Document
from typing_extensions import List, TypedDict

from langgraph.graph import START, StateGraph
from langchain.chat_models import init_chat_model

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

    
def init(context):
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

    chat_service_url = os.environ["CHAT_SERVICE_URL"]
    
    os.environ["OPENAI_API_KEY"] = "ignore"

    llm = init_chat_model("chatmodel", model_provider="openai", base_url=f"http://{chat_service_url}/openai/v1/")
    prompt = hub.pull("rlm/rag-prompt")

    def retrieve(state: State):
        retrieved_docs = vector_store.similarity_search(state["question"])
        return {"context": retrieved_docs}
    
    def generate(state: State):
        docs_content = "\n\n".join(doc.page_content for doc in state["context"])
        messages = prompt.invoke({"question": state["question"], "context": docs_content})
        response = llm.invoke(messages)
        return {"answer": response.content}

    graph_builder = StateGraph(State).add_sequence([retrieve, generate])
    graph_builder.add_edge(START, "retrieve")
    graph = graph_builder.compile()

    setattr(context, "graph", graph)

def serve(context, event):
    graph = context.graph
    context.logger.info(f"Received event: {event}")
    
    if isinstance(event.body, bytes):
        body = json.loads(event.body)
    else:
        body = event.body
        
    question = body["question"]
    response = graph.invoke({"question": question})
    return {"answer": response["answer"]}
    