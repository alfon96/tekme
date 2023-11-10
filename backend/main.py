from fastapi import FastAPI
from routers.teachers import teachers
from routers.users import users
from fastapi.middleware.cors import CORSMiddleware

import debugpy

debugpy.listen(("0.0.0.0", 5678))
print("⏳ VS Code debugger can now attach, press F5 in VS Code ⏳", flush=True)
debugpy.wait_for_client()


app = FastAPI()

origins = [
    "http://localhost:3000",  # React's default dev server
    "http://0.0.0.0:5678",  # Debug server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(teachers)
app.include_router(users)
