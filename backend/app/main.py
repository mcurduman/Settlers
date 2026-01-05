# # main.py - generic FastAPI app
# from fastapi import FastAPI
# import uvicorn

# app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/health")
# def health_check():
#     return {"status": "ok"}


# if __name__ == "__main__":
#     uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)
n = int(input())
try:
    res = n // 0
except ZeroDivisionError:
    print(1)
else:
    print(2)
finally:
    print(3)
