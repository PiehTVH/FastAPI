from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBookingInfo
from app.users.dependencies import get_current_user


from app.users.models import Users

router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"]
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def start_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/bookings", response_class=HTMLResponse)
async def booking_page(
    request: Request,
    ):
    try:
        user: Users = Depends(get_current_user)
    except:
        user = None
    return templates.TemplateResponse("booking.html", {"request": request, "user": user})

@router.get("/my_bookings", response_class=HTMLResponse)
async def my_bookings(
    request: Request,
    user: Users = Depends(get_current_user)):
    res = await BookingDAO.find_all_with_images(user_id=user.id)
    return templates.TemplateResponse("my_bookings.html", {"request": request, "bookings": res})