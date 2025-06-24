import os
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI, LlamaCpp
from src.retriever import get_retriever

load_dotenv()

class Inference:
    """Wraps a RetrievalQA chain over a FAISS index and LLM backend."""
    def __init__(self):
        use_local = os.getenv("USE_LOCAL_LLM", "false").lower() == "true"
        if use_local:
            self.llm = LlamaCpp(model_path=os.getenv("LLM_MODEL_PATH"))
        else:
            self.llm = OpenAI()

        k = int(os.getenv("RETRIEVER_K", 4))
        self.retriever = get_retriever(k=k)
        self.qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
        )

    def answer(self, question: str):
        return self.qa({"query": question})

if __name__ == "__main__":
    inf = Inference()
    print(inf.answer("What is FAISS?"))
