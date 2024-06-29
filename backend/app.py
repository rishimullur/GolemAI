from fastapi import FastAPI, HTTPException
from helper.context import save, retrieve
from schemas.schemas import UserBase, ChatBase, MessageBase, ChatID
from golem.app import llama_chat
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
def process(chat_id_input: ChatID):

    try:
        chat_id = chat_id_input.chat_id

        context_dict = retrieve(chat_id)

        concat_chat = context_dict["concat_chat"]

        # if min_responses < 4:
        #     return HTTPException(status_code=200, detail={"status": "success", "message": "Not enough responses to process"})

        response = llama_chat(concat_chat)

        print("End llama req")

        return HTTPException(status_code=200, detail={"status": "success", "response": response})

    except Exception as e:
        raise HTTPException(status_code=400, detail={"status": "error", "message": str(e), "chat_id": chat_id})

#END TD

if __name__ == "__main__":
    print("Starting server...")
    uvicorn.run("app:app", host="localhost", port=8005, use_colors=False)
    print("Server stopped.")