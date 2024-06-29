from fastapi import FastAPI
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
def save_chat():
    ...

@app.post("/process")
def process():
    ...

#END TD

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8005)