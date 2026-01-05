from fastapi import FastAPI
import uvicorn

from app.api.error_handler import register_error_handlers
from app.api.routes import router

app = FastAPI()

register_error_handlers(app)
app.include_router(router, prefix="/api")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)
