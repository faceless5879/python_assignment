from fastapi import FastAPI
from .routers import financial

app = FastAPI()

app.include_router(financial.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
