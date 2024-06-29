from fastapi import FastAPI
import uvicorn
from golem.app import llama_chat 

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.get("/chat")
def chat():
    llama_chat("What is the capital of France?")
    # return {"chat": "chat"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8005)