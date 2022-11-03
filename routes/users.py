from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from auth.jwt_handler import create_access_token
from models.users import User, UserSignIn, TokenResponse
from database.connection import Database
from auth.hash_password import HashPassword

user_route = APIRouter(
    tags=["User"]
)

users_db = Database(User)
hash_password = HashPassword()


@user_route.post('/signup')
async def sign_up_user(new_user: User) -> dict:
    check_existence = await User.find_one(User.email == new_user.email)
    if check_existence:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email Address Already exists"
        )
    hashed_password = hash_password.create_hash(new_user.password)
    new_user.password = hashed_password
    await users_db.create_db(new_user)
    return {"Message": "User Successfully Signed Up"}


@user_route.post('/signin', response_model=TokenResponse)
async def sign_in_user(current_user: OAuth2PasswordRequestForm = Depends()) -> dict:
    user_exist = await User.find_one(User.email == current_user.username)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found{user_exist}"
        )
    if hash_password.verify_hash(current_user.password, user_exist.password):
        access_token = create_access_token(user_exist.email)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }
    # if user_exist.password == current_user.password:
    #     return {
    #         "Message": "Sign in Successful"
    #     }
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Incorrect password"
    )
