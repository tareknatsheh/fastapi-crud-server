import pytest
import utils.auth_helper as auth
from fastapi import HTTPException

def test_hash_password():
    pwd = "hello123"
    hashed_pwd = auth.hash_password(pwd)

    assert len(hashed_pwd.decode('utf-8')) == 60

def test_generate_jwt_token():
    jwt_token = auth.generate_jwt_token({"role": "test"})
    assert jwt_token == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoidGVzdCJ9.hbOf_lFaJIryl9h6c3gvQyR6-x4C-K63xvkrYKjA6ho"

def test_verify_password():
    assert auth.verify_password("$2b$12$L9i1ZArZHm0wGT7.sqCdMeu/5vYHz8jdAlEYIE.IurDzOq4sEzV12", "r123")

def test_add_new_user_username_not_empty():
    with pytest.raises(HTTPException) as exc_info:
        auth.add_new_user("", "pwd", "guest")
    assert isinstance(exc_info.value, HTTPException)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "username must be at least 3 characters"

def test_add_new_user_password_not_empty():
    with pytest.raises(HTTPException) as exc_info:
        auth.add_new_user("good user name", "", "guest")
    assert isinstance(exc_info.value, HTTPException)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "password must be at least 3 characters"