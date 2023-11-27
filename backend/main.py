from fastapi import FastAPI
from routers.users import users
from routers.classes import classes
from routers.scores import scores
from routers.admins import admins

from fastapi.middleware.cors import CORSMiddleware

import debugpy


def create_app():
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

    app.include_router(admins)
    app.include_router(users)
    app.include_router(classes)
    app.include_router(scores)

    return app


debugpy.listen(("0.0.0.0", 5678))
print("⏳ VS Code debugger can now attach, press F5 in VS Code ⏳", flush=True)
debugpy.wait_for_client()
app = create_app()

if __name__ == "__main__":
    debugpy.listen(("0.0.0.0", 5678))
    print("⏳ VS Code debugger can now attach, press F5 in VS Code ⏳", flush=True)
    debugpy.wait_for_client()
    app = create_app()
