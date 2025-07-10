from fastapi import FastAPI
from pydantic import EmailStr, BaseModel

import uvicorn

app = FastAPI()


class CreateUser(BaseModel):
    email: EmailStr


@app.get("/")
def hello_index():
    return {
        "message": "Hello index!"
    }


@app.get("/hello/")
def hello(name: str = "World"): # This func have defaults: "World"
    name = name.strip().title() # Spaces is removed by strip()
    return {"message": f"Hello {name}"}


# Endpoint with email validator from pydantic
@app.post("/users/")
def create_user(user: CreateUser):
    return {
        "message": "success",
        "email": user.email,
    }


@app.get("/calc/add")
def add(a: int, b: int):
    return {
        "a": a,
        "b": b,
        "result": a + b
    }


@app.get("/items")
def list_items():
    return [
        "item1",
        "item2",
        "item3",
        ]


# It's important to use right order of endpoints, because if this endpoint was after "/items/{item_id}/", It will be processing by first endpoint and giving error 422, because dict != int
@app.get("/items/latest/")
def get_latest_item():
    return {"item": {"id": "0", "name": "latest"}}


# Endpoint with type annotation
@app.get("/items/{item_id}/")
def get_item_by_id(item_id: int):
    return {
        "item": {
            "id": item_id
        }
    }


# Uvicorn config for simply script run
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)