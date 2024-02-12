from datetime import date, datetime
import uuid
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBookingInfo
from app.cart.dao import CartDao
from app.exceptions import TokenExpiredException, UserIsNotPresentException
from app.favourites.dao import FavDao
from app.hotels.dao import HotelsDAO
from app.hotels.rooms.dao import RoomsDAO
from app.cart.dao import CartDao
from app.users.dependencies import  get_current_user
from app.users.models import Users


from app.users.models import Users

router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"]
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/clear", response_class=HTMLResponse)
async def clear_page(request: Request):
    return templates.TemplateResponse("clear.html", {"request": request})

@router.get("", response_class=HTMLResponse)
async def start_page(
    request: Request,
    ):
    len_cart = 0
    len_fav = 0
    if (anonimous_id := request.cookies.get("cart")):   
        len_cart = len(await CartDao.find_all_with_images(anonimous_id=anonimous_id))
        len_fav = len(await FavDao.find_all(anonimous_id=anonimous_id))
    return templates.TemplateResponse("index.html", {"request": request, "cart_count": len_cart, "fav_count": len_fav})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/reg_user", response_class=HTMLResponse)
async def reg_user(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/bookings", response_class=HTMLResponse)
async def booking_page(
    request: Request,
    user: Users = Depends(get_current_user),
    ):
    len_fav = len(await FavDao.find_all(user_id=user.id))    
    len_bookings = len(await BookingDAO.find_all_with_images(user_id=user.id))
    len_cart = len(await CartDao.find_all_with_images(user_id=user.id)) 
    return templates.TemplateResponse("booking.html", {"request": request, "user": user.email, "book_count": len_bookings, "cart_count": len_cart, "fav_count": len_fav})
    
@router.get("/anon_bookings", response_class=HTMLResponse)
async def anon_booking_page(
    request: Request,
    response: Response,
    ):
    if not (anonimous_id := request.cookies.get("cart")):
        anonimous_id = str(uuid.uuid4())
        response.set_cookie("cart", anonimous_id, httponly=True)
    len_fav = len(await FavDao.find_all(anonimous_id=anonimous_id))    
    len_cart = len(await CartDao.find_all_with_images(anonimous_id=anonimous_id)) 
    return templates.TemplateResponse("anon_booking.html", {"request": request, "cart_count": len_cart, "fav_count": len_fav})


@router.get("/my_bookings", response_class=HTMLResponse)
async def my_bookings(
    request: Request,
    user: Users = Depends(get_current_user)):
    res = await BookingDAO.find_all_with_images(user_id=user.id)
    return templates.TemplateResponse("my_bookings.html", {"request": request, "bookings": res})

@router.get("/hotels", response_class=HTMLResponse)
async def get_hotels_by_loc_date(request: Request,
    location: str, date_from: date, date_to: date,
    ):
    res = await HotelsDAO.find_all(location, date_from, date_to)
    return templates.TemplateResponse("hotels_by_loc_and_time.html", {"request": request, "hotels": res})

@router.get("/search", response_class=HTMLResponse)
async def search_page(request: Request):
    return templates.TemplateResponse("search_hotels.html", {"request": request})

@router.get("/hotels/{hotel_id}/rooms", response_class=HTMLResponse)
async def get_rooms_by__date(
    request: Request,
    response: Response,
    hotel_id: int, 
    date_from: date, 
    date_to: date,
    ):
    fav = []
    if (user_id := request.cookies.get("user_id")):
        fav = await FavDao.find_all(user_id=int(user_id))
    else:
        if not (anonimous_id := request.cookies.get("cart")):
            anonimous_id = str(uuid.uuid4())
            response.set_cookie("cart", anonimous_id, httponly=True)
        fav = await FavDao.find_all(anonimous_id=anonimous_id)
    fav = [f.room_id for f in fav]
    res = await RoomsDAO.find_all(hotel_id, date_from, date_to)
    return templates.TemplateResponse("rooms_by__time.html", {"request": request, "rooms": res, "fav": fav})
    
@router.get("/cart", response_class=HTMLResponse)
async def get_my_cart(
    request: Request,
    user: Users = Depends(get_current_user),
    ):
    res = await CartDao.find_all_with_images(user_id=user.id)
    fav = await FavDao.find_all(user_id=user.id)
    fav = [f.room_id for f in fav]
    return templates.TemplateResponse("my_cart.html", {"request": request, "bookings": res, "date": datetime.now().date(), "fav": fav})

@router.get("/cart/anon", response_class=HTMLResponse)
async def get_anon_cart(
    request: Request,
    response: Response,
    ):
    if not (anonimous_id := request.cookies.get("cart")):
        anonimous_id = str(uuid.uuid4())
        response.set_cookie("cart", anonimous_id, httponly=True)
    res = await CartDao.find_all_with_images(anonimous_id=anonimous_id)
    return templates.TemplateResponse("anon_cart.html", {"request": request, "bookings": res, "date": datetime.now().date()})

@router.get("/my_fav", response_class=HTMLResponse)
async def get_my_fav(
    request: Request,
    user: Users = Depends(get_current_user),
):
    res = await FavDao.get_all_fav(user_id=user.id)
    return templates.TemplateResponse("all_my_fav.html", {"request": request, "rooms": res})

@router.get("/anon_fav", response_class=HTMLResponse)
async def get_anon_fav(
    request: Request,
    response: Response,
):
    if not (anonimous_id := request.cookies.get("cart")):
        anonimous_id = str(uuid.uuid4())
        response.set_cookie("cart", anonimous_id, httponly=True)
    res = await FavDao.get_all_fav(anonimous_id=anonimous_id)
    return templates.TemplateResponse("all_anon_fav.html", {"request": request, "rooms": res})

@router.get("/fav_by_date")
async def get_fav_by_date(
    request: Request,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
):
    res = await FavDao.get_fav_by_date(date_from, date_to, user_id=user.id)
    return templates.TemplateResponse("all_my_fav_by_date.html", {"request": request, "rooms": res})

@router.get("/anon_fav_by_date")
async def get_anon_fav_by_date(
    request: Request,
    response: Response,
    date_from: date,
    date_to: date,
):
    if not (anonimous_id := request.cookies.get("cart")):
        anonimous_id = str(uuid.uuid4())
        response.set_cookie("cart", anonimous_id, httponly=True)
    res = await FavDao.get_fav_by_date(date_from, date_to, anonimous_id=anonimous_id)
    return templates.TemplateResponse("all_my_fav_by_date.html", {"request": request, "rooms": res})