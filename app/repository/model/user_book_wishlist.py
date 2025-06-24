# app/repository/model/user_book_wishlist.py
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.repository.model import Base


class UserBookWishlist(Base):
    __tablename__ = "user_wishlist"

    id:       Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id:  Mapped[int] = mapped_column(ForeignKey("users_details.id"))
    book_id:  Mapped[int] = mapped_column(ForeignKey("books.id"))
