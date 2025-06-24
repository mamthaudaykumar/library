# models/__init__.py

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from app.repository.model.book import Book
from app.repository.model.user_book_borrow import BookBorrowStatus
from app.repository.model.user_details import UsersDetails
from app.repository.model.user_book_wishlist import UserBookWishlist
# ...add new imports as you create new model files
