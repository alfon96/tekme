from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional
from schemas.schemas import SignUpModel, SignInModel
from crud import crud
from pymongo.database import Database
from utils import encryption
from db.db_handler import get_db
from pymongo import errors as pymongo_errors

users = APIRouter(prefix="/users")


@users.post("/signup")

# Assuming a function to validate tokens
async def verify_token(authorization: str = Header(...)):
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Invalid or missing authorization header"
        )

    # Extract token from the authorization header
    token = authorization.split(" ")[1]

    if not encryption.check_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")


async def signup(user_details: SignUpModel, db: Database = Depends(get_db)):
    try:
        # Cripta la password
        hashed_password = encryption.encrypt_password(user_details.password)

        # Prepara i dati dell'utente per l'inserimento nel DB
        user_data = {
            "name": user_details.name,
            "surname": user_details.surname,
            "birth_date": user_details.birth_date,
            "phone": user_details.phone,
            "email": user_details.email,
            "password": hashed_password,
        }

        # Crea l'utente nel DB e ricava l'id
        user_id = crud.create_user(user_details.role, user_data, db).inserted_id

        # Crea un token JWT per l'utente appena creato
        token = encryption.create_jwt_token(str(user_id), user_details.role)
        return {"token": token, "message": "User created successfully"}

    except pymongo_errors.DuplicateKeyError:
        raise HTTPException(
            status_code=400, detail="Email or phone number already exists"
        )
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@users.post("/signin")
async def signin(credentials: SignInModel, role: str, db: Database = Depends(get_db)):
    # Cerca l'utente
    user = crud.get_user_by_email(role, credentials.email, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Verifica la password
    if not encryption.check_password(credentials.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Crea un token JWT
    token = encryption.create_jwt_token(str(user["_id"]), role)

    return {"token": token, "user_id": str(user["_id"]), "role": role}


@users.get("/classes/{class_name}")
async def get_class(
    class_name: str, _: str = Depends(verify_token), db: Database = Depends(get_db)
):
    try:
        class_data = crud.get_class_by_name(class_name, db)
        if not class_data:
            raise HTTPException(status_code=404, detail="No data found for this class")

        return {**class_data, "_id": str(class_data["_id"])}

    # except SomeMongoDBException as e:
    #     raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
