# ====== Main Python file ====== #

from contextlib import asynccontextmanager

from fastapi import FastAPI

import uvicorn

from core.config import settings
from items_views import router as items_router
from users.views import router as users_router
from api_v1.products.views import router as router_v1

@asynccontextmanager
async def lifespan(app: FastAPI):  # The lifespan of main app
    ...
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router_v1, prefix=settings.api_v1_prefix)
app.include_router(items_router)
app.include_router(users_router)


@app.get("/")
def hello_index():
    return {"message": "Hello index!"}


@app.get("/hello/")
def hello(name: str = "World"):  # This func have defaults: "World"
    name = name.strip().title()  # Spaces is removed by strip()
    return {"message": f"Hello {name}"}


@app.get("/calc/add")
def add(a: int, b: int):
    return {"a": a, "b": b, "result": a + b}


# Uvicorn config for simply script run
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)


# ====== Listening on 127.0.0.1:8000 ====== #
