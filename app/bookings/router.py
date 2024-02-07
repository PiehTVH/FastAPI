from datetime import date
from urllib import response

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import TypeAdapter
from sqlalchemy import select
from fastapi_versioning import version

from app.bookings.dao import BookingDAO
from app.bookings.models import Bookings
from app.bookings.schemas import SBooking, SBookingInfo, SNewBooking
from app.exceptions import RoomCannotBeBooked
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
#@version(1)
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookingInfo]:
    return await BookingDAO.find_all_with_images(user_id=user.id)


@router.post("")
#@version(1)
async def add_booking(
    booking: SNewBooking,
    user: Users = Depends(get_current_user)
) -> SNewBooking:
    booking = await BookingDAO.add(
        user.id,
        booking.room_id,
        booking.date_from,
        booking.date_to)
    if not booking:
        raise RoomCannotBeBooked
    booking = TypeAdapter(SNewBooking).validate_python(booking).model_dump()
    send_booking_confirmation_email.delay(booking, "chepalin@yandex.ru")
    return booking


@router.delete("/{booking_id}")
#@version(1)
async def delete_booking(
    booking_id: int,
    user: Users = Depends(get_current_user),
):
    res = await BookingDAO.delete(booking_id=booking_id, user_id=user.id)
    return res


@router.get('/notice', status_code=201)
async def get_notice_list(
    delta:int
) :
    res = await BookingDAO.find_all_nearest_bookings(delta)
    return res
