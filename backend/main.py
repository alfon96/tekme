from fastapi import FastAPI
from routers.teachers import teachers

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(teachers)