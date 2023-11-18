from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional, Union
from schemas import schemas
from crud import crud
from pymongo.database import Database
from utils import encryption
from db.db_handler import get_db
from pymongo import errors as pymongo_errors
from utils.setup import Setup

users = APIRouter(prefix="/users")


@users.post("/signup")
async def signup(
    user_data: schemas.Signup,
    subjects: Optional[list[str]] = [],
    details: Optional[list[str]] = [],
    db: Database = Depends(get_db),
):
    try:
        # Cripta la password
        hashed_password = encryption.encrypt_password(user_data.password)
        user_data.password = hashed_password

        user_role = user_data.role
        new_user = {**user_data.dict()}

        if user_role == "teachers":
            if len(subjects) == 0:
                raise HTTPException(status_code=422, detail="Missing subject field!")
            new_user["subjects"] = subjects

        elif user_role == "students":
            new_user["details"] = details

        # Crea l'utente nel DB e ricava l'id
        user_id = await crud.create_user(user_data.role, new_user, db)

        # Crea un token JWT per l'utente appena creato
        token = encryption.create_jwt_token(str(user_id), user_data.role)
        return {"token": token, "message": "User created successfully"}

    except pymongo_errors.DuplicateKeyError:
        raise HTTPException(
            status_code=400, detail="Email or phone number already exists"
        )
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        return HTTPException(status_code=500, detail=f"An exception occurred: {str(e)}")


@users.post("/signin")
async def signin(
    credentials: schemas.Signin,
    db: Database = Depends(get_db),
):
    # Cerca l'utente
    try:
        user = await crud.get_user_by_email(credentials.role, credentials.email, db)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Verifica la password
        if not encryption.check_password(credentials.password, user["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Crea un token JWT
        token = encryption.create_jwt_token(str(user["_id"]), credentials.role)

        return {
            "token": token,
            f"{Setup.id}": str(user["_id"]),
            f"{Setup.role}": credentials.role,
        }
    except Exception as e:
        return HTTPException(status_code=500, detail=f"An exception occurred: {str(e)}")


@users.get("/")
async def read_user(
    token_payolad: dict = Depends(encryption.read_token),
    db: Database = Depends(get_db),
) -> Union[schemas.RelativeBase, schemas.StudentBase, schemas.TeacherBase]:
    try:
        user_id = token_payolad[f"{Setup.id}"]
        user_role = token_payolad[f"{Setup.role}"]
        user_data = await crud.read_user(user_role, user_id, db)

        if user_role == schemas.User.TEACHER:
            return schemas.TeacherBase(**user_data)
        elif user_role == schemas.User.STUDENT:
            return schemas.StudentBase(**user_data)
        elif user_role == schemas.User.RELATIVE:
            return schemas.RelativeBase(**user_data)
        else:
            raise HTTPException(status_code=404, detail="User role not found")

    except Exception as e:
        return HTTPException(status_code=500, detail=f"An exception occurred: {str(e)}")


@users.patch("/")
async def update_user(
    update_data: dict,
    token_payolad: dict = Depends(encryption.read_token),
    db: Database = Depends(get_db),
):
    try:
        user_id = token_payolad[f"{Setup.id}"]
        user_role = token_payolad[f"{Setup.role}"]

        if user_role == schemas.User.TEACHER:
            if not schemas.check_keys_in_schema(
                schemas.TeacherSensitiveData, update_data
            ):
                raise ValueError("The input keys do not match with the Teacher schema!")

        elif user_role == schemas.User.STUDENT:
            if not schemas.check_keys_in_schema(
                schemas.StudentSensitiveData, update_data
            ):
                raise ValueError("The input keys do not match with the Student schema!")

        elif user_role == schemas.User.RELATIVE:
            if not schemas.check_keys_in_schema(
                schemas.RelativeSensitiveData, update_data
            ):
                raise ValueError(
                    "The input keys do not match with the Relative schema!"
                )

        else:
            raise HTTPException(
                status_code=404, detail="User role seems to not exists in the database."
            )

        modified = await crud.update_document(user_role, user_id, update_data, db)
        if not modified == 1:
            return HTTPException(
                status_code=400, detail="Fields have NOT been modified."
            )

        return HTTPException(
            status_code=200, detail="Fields have been modified succesfully"
        )
    except Exception as e:
        return HTTPException(status_code=500, detail=f"An exception occurred: {str(e)}")


@users.delete("/")
async def delete_user(
    password: str,
    token_payolad: dict = Depends(encryption.read_token),
    db: Database = Depends(get_db),
):
    try:
        user_id = token_payolad[f"{Setup.id}"]
        user_role = token_payolad[f"{Setup.role}"]
        user_data = await crud.read_user(user_role, user_id, db, sensitive_data=True)
        if not encryption.check_password(password, user_data["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        await crud.delete_document(user_role, user_id, db)

        return HTTPException(status_code=200, detail="User was deleted")
    except Exception as e:
        return HTTPException(status_code=500, detail=f"An exception occurred: {str(e)}")
