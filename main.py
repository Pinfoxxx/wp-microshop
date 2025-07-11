from typing import Annotated

from fastapi import FastAPI, Path
from pydantic import EmailStr, BaseModel

import uvicorn

from items_views import router as items_router
from users.views import router as users_router

app = FastAPI()
app.include_router(items_router)
app.include_router(users_router)


@app.get("/")
def hello_index():
    return {
        "message": "Hello index!"
    }


@app.get("/hello/")
def hello(name: str = "World"): # This func have defaults: "World"
    name = name.strip().title() # Spaces is removed by strip()
    return {"message": f"Hello {name}"}


@app.get("/calc/add")
def add(a: int, b: int):
    return {
        "a": a,
        "b": b,
        "result": a + b
    }


# Uvicorn config for simply script run
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)