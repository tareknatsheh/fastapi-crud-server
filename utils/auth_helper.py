import utils.db_helper as db
from decouple import config
import bcrypt
import json
import jwt
from fastapi import  Header, HTTPException
from typing import Annotated


JWT_SECRET = config("secret")
AUTH_USERS_DB = "./data/auth_db.json"

ROLES = ["admin", "guest"]

def hash_password(password: str) -> bytes:
    bytes = password.encode('utf-8') 
    salt = bcrypt.gensalt() 
    hash = bcrypt.hashpw(bytes, salt)
    return hash


def get_user(username) -> dict | None:
    all_users = db.get_data(AUTH_USERS_DB)
    if username in all_users:
        return all_users[username]
    return None

def add_new_user(username: str, password: str, role: str = "guest") -> bool:
    if len(username) < 3:
        raise HTTPException(status_code=400, detail="username must be at least 3 characters")
    if len(password) < 3:
        raise HTTPException(status_code=400, detail="password must be at least 3 characters")
    try:
        all_users = db.get_data(AUTH_USERS_DB)
        all_users[username] = {
            "username": username,
            "password": hash_password(password).decode('utf-8'),
            "role": role
        }
        db.write_data(AUTH_USERS_DB, all_users)
        return True
    except Exception as error:
        print(f"Error: {error}")
        return False


def generate_jwt_token(payload) -> str:
    token: str = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return token

def get_data(file_path):
    with open(file_path) as f:
        data = json.load(f)
        return data


def verify_password(stored, from_user) -> bool:
    return bcrypt.checkpw(from_user.encode('utf-8'), stored.encode('utf-8'))


def verify_jwt(user_jwt):
    try:
        data = jwt.decode(user_jwt, JWT_SECRET, algorithms=["HS256"])
        return data["role"]
    except Exception as e:
        print('error: ', e)
        print("bad token")
        raise HTTPException(status_code=498, detail="Invalid token")


async def verify_admin(token: Annotated[str, Header(...)]):
    role = verify_jwt(token)
    return role == "admin"

async def verify_user(token: Annotated[str, Header(...)]):
    return verify_jwt(token) in ROLES