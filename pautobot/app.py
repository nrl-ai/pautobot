import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from pautobot.engine import qa_instance
from pautobot.models import Query
from pautobot.utils import extract_frontend_dist
from pautobot import global_state

static_folder = "pautobot-data/frontend-dist"


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def think(query):
    global_state.global_answer = {
        "status": "THINKING",
        "answer": "",
        "docs": [],
    }
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
        global_state.global_answer = {
            "status": "READY",
            "answer": answer,
            "docs": doc_json,
        }
    except Exception as e:
        print("Error during thinking: ", e)
        global_state.global_answer = {
            "status": "ERROR",
            "answer": None,
            "docs": None,
        }


@app.post("/api/ask")
async def ask(query: Query, background_tasks: BackgroundTasks):
    if global_state.global_answer["status"] == "THINKING":
        raise Exception("I am still thinking!")
    global_state.global_answer = {
        "status": "THINKING",
        "answer": "",
        "docs": [],
    }
    background_tasks.add_task(think, query.query)
    return {"message": "Query received"}


@app.get("/api/get_answer")
async def get_answer():
    return global_state.global_answer


app.mount("/", StaticFiles(directory=static_folder, html=True), name="static")


def main():
    extract_frontend_dist(static_folder)
    uvicorn.run(app, host="0.0.0.0", port=5678)


if __name__ == "__main__":
    main()
