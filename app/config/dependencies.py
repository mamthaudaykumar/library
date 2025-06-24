from fastapi import Depends
from sqlalchemy.orm import Session

from config.cfg_sql_connection import get_db
from repository.dao.book_dao import BookDAO
# from service.notification_service import NotificationService
from service.user_wishlist_service import UserWishlistService


def get_book_dao(db: Session = Depends(get_db)) -> BookDAO:
    return BookDAO(db)

def get_user_wishlist_service(db: Session = Depends(get_db)) -> UserWishlistService:
    return UserWishlistService(db)

# def get_notification_service(
#     wishlist_service: UserWishlistService = Depends(get_user_wishlist_service),
# ) -> NotificationService:
#     return NotificationService(wishlist_service)