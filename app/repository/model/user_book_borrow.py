from datetime import datetime
from sqlalchemy import ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.repository.model import Base
class BookBorrowStatus(Base):
    __tablename__ = "user_book_borrow_details"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users_details.id"), nullable=False)  # typically user_id is int
    borrowed_on: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # e.g., 'BORROWED', 'RETURNED', 'LOST'
    updated_on: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_on: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
