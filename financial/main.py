from fastapi import FastAPI, Request
from .routers import financial
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    detail = exc.errors()[0]["msg"]
    return JSONResponse(content={"info": detail}, status_code=400)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    detail = exc.errors()[0]["msg"]
    return JSONResponse(content={"info": detail}, status_code=400)


app.include_router(financial.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
