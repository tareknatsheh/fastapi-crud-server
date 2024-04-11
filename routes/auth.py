from fastapi import APIRouter, HTTPException, Request
from models.auth_models import Auth_Model
from utils import auth_helper as auth
from utils.decorators import handle_errors, log_it

router = APIRouter()

@router.post('/auth/sign_up')
@handle_errors
@log_it
def sign_up(request: Request, body:Auth_Model) -> dict[str, str]:
    """Sign up for a new user account

    Args:
        body (Auth_Model): user credentials (username and password)

    Returns:
        dict: wether the sign up succeeded or failed, and a token for future requests
    """
    user = auth.get_user(body.username)
    if user:
        raise HTTPException(status_code=400, detail="username is taken")

    user_creation_result = auth.add_new_user(body.username, body.password)
    if not user_creation_result:
        raise HTTPException(status_code=400, detail="User creation failed")
    
    # let's create a JWT token for the user
    jwt_token = auth.generate_jwt_token({"role": "guest"})
    return {"msg": "User creation succeeded", "token": jwt_token}
    # return dict(user_creation_result)

@router.post('/auth/sign_in')
@handle_errors
@log_it
def sign_in(request: Request, body:Auth_Model) -> dict[str, str]:
    """Sign registered users in and return a token

    Args:
        body (Auth_Model): user sign in details (username and password)

    Returns:
        dict: sign-in result. If succeeded it returns a token that has role info for fututre requests
    """
    user = auth.get_user(body.username)
    if user:
        stored_password = user["password"]
        is_password_correct = auth.verify_password(stored_password, body.password)
        if not is_password_correct:
            raise HTTPException(status_code=401, detail="Wrong username or password")
        # check their role:
        role: str = user["role"]
        token: str = auth.generate_jwt_token({"role": role})
        return {"msg": f"{user['username']} sing-in successful","token": token}
    else:
        raise HTTPException(status_code=401, detail="Wrong username or password")
