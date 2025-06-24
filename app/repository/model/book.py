from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.repository.model import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    book_id: Mapped[int] = mapped_column(Integer, nullable=False)
    isbn: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)  # fixed typo
    publication_year: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String, nullable=False)
    language: Mapped[str] = mapped_column(String)