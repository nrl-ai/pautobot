import copy

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from pautoengine.engine import qa_instance

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


is_thinking = False
global_answer = None


def think(query):
    global global_answer, is_thinking
    global_answer = None
    try:
        print("Received query: ", query)
        print("Thinking...")
        res = qa_instance(query)
        answer, docs = (
            res["result"],
            res["source_documents"],
        )
        doc_json = []
        for document in docs:
            doc_json.append(
                {
                    "source": document.metadata["source"],
                    "content": document.page_content,
                }
            )
        global_answer = {"answer": answer, "docs": doc_json}
    except Exception as e:
        print("Error during thinking: ", e)
        global_answer = {"answer": None, "docs": None}
    is_thinking = False


class Query(BaseModel):
    query: str


@app.post("/api/ask")
async def ask(query: Query, background_tasks: BackgroundTasks):
    global is_thinking
    if is_thinking:
        raise Exception("I am working on previous query. Please wait.")
    is_thinking = True
    background_tasks.add_task(think, query.query)
    return {"message": "Query received"}


@app.get("/api/get_answer")
async def get_answer():
    global global_answer
    if global_answer is None:
        return {"status": "THINKING", "answer": None, "docs": None}
    answer = copy.deepcopy(global_answer)
    global_answer = None
    return {
        "status": "READY",
        "answer": answer["answer"],
        "docs": answer["docs"],
    }
