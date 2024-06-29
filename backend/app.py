from fastapi import FastAPI, HTTPException
from helper.context import save, retrieve
from schemas.schemas import UserBase, ChatBase, MessageBase
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

#TODO: Mike

@app.post("/chat")
def save_chat(user_base: UserBase, chat_base: ChatBase, message_base: MessageBase):
    try:
        save(user_base, chat_base, message_base)
        return HTTPException(status_code=200, detail={"status": "success", "message": "Chat saved successfully"})

    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e)})


@app.post("/process")
def process():
    ...

#END TD

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8005)