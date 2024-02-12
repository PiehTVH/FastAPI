
from fastapi import APIRouter, Depends, Request, Response
from app.cart.dao import CartDao
from app.exceptions import CannotAddDataToDatabase, IncorrectEmailOrPasswordException, UserAlreadyExistsException
from app.favourites.dao import FavDao
from app.users.dao import UsersDAO
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dependencies import get_current_admin_user, get_current_user
from app.users.models import Users

from app.users.schemas import SUserAuth

router_users = APIRouter(
    prefix ="/auth",
    tags = ["Auth & Пользователи"],
)

router_auth = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

@router_auth.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    new_user = await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)
    if not new_user:
        raise CannotAddDataToDatabase

@router_auth.post("/login")
async def login_user(request: Request, response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    response.set_cookie("user_id", user.id, httponly=True)
    if (anonimous_id := request.cookies.get("cart")):
        res = await CartDao.from_anon_to_reg(anonimous_id=anonimous_id, user=user)
        res_1 = await FavDao.from_anon_to_reg(anonimous_id=anonimous_id, user=user)
    return access_token



@router_auth.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")
    response.delete_cookie("user_id")



@router_users.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user


@router_users.get("/all")
async def read_users_all(current_user: Users = Depends(get_current_admin_user)):
    return await UsersDAO.find_all()
