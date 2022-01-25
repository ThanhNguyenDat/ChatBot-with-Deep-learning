from fastapi import FastAPI
from pydantic import BaseModel


class MyItem(BaseModel):
    name: str
    price: float
    ready: int


app = FastAPI()


@app.get("/")
async def home():
    return "Home ne"

@app.post("/submit")
async def submit(item: MyItem):
    print(item)
    return "Save thành công"
