# app/repository/dao/book_dao.py
from datetime import datetime
from typing import List, Literal, Optional
from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session, aliased
from app.repository.model.book import Book
from app.repository.model.user_book_borrow import BookBorrowStatus
from repository.model import UsersDetails
from repository.model.user_borrow_details import StatusDetailsDTO
from schema.request.book_borrow_status import BookBorrowStatusRequest


class BookDAO:
    def __init__(self, db: Session):
        self.db = db

    def create(self, book: Book) -> Book:
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def update(self, id: int, updated: Book) -> Book:
        book = self.db.get(Book, id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        for key, value in updated.model_dump().items():
            setattr(book, key, value)
        self.db.commit()
        self.db.refresh(book)
        return book

    def get_one(self, book_id: int) -> Book:
        book = self.db.get(Book, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book

    def get_book_status_details(self, status: str, book_id: int) -> Book:
        status = (
            self.db.query(BookBorrowStatus, UsersDetails)
            .join(UsersDetails, BookBorrowStatus.user_id == UsersDetails.id)
            .filter(
                BookBorrowStatus.book_id == book_id,
                BookBorrowStatus.status == status  # Only current status
            )
            .order_by(BookBorrowStatus.borrowed_on.desc())
            .first()
        )

        if status:
            borrow_status, borrower = status
            status_details = StatusDetailsDTO(
                status=borrow_status.status,
                borrowerId=borrower.id,
                borrowerName=borrower.name,
                borrowedOn=borrow_status.borrowed_on.strftime("%Y-%m-%d"),
            )
        else:
            status_details = StatusDetailsDTO(
                status="AVAILABLE",
                borrowerId=0,
                borrowerName="N/A",
                borrowedOn=None,
            )
        return status_details

    def get_all(self) -> List[Book]:
        return self.db.query(Book).all()

    def update_status(self, req: BookBorrowStatusRequest) -> None:
        book_status = self.db.query(BookBorrowStatus).filter_by(status="RENTED").first()
        if book_status:
            raise HTTPException(status_code=404, detail="Book is already rented")
        data = Book
        self.db.commit()
        self.db.refresh(book_status)

    def get_all_with_status(self, borrow_status: str = "RENTED") -> list[tuple[Book, StatusDetailsDTO]]:
        """
        Returns a list of (book, status_details_dto) tuples.
        If a book has no active record with `borrow_status`, status_details_dto
        will contain "AVAILABLE".
        """
        u = aliased(UsersDetails)  # avoid name clashes
        bs = aliased(BookBorrowStatus)

        stmt = (
            select(Book, bs, u)
            .join(bs, bs.book_id == Book.id, isouter=True)
            .join(u, u.id == bs.user_id, isouter=True)
            .where((bs.status == borrow_status) | (bs.status.is_(None)))
        )

        raw_rows: list[tuple[Book, BookBorrowStatus | None, UsersDetails | None]] = self.db.execute(stmt).all()

        result: list[tuple[Book, StatusDetailsDTO]] = []
        for book, borrow_status_row, borrower_row in raw_rows:
            if borrow_status_row is None:
                dto = StatusDetailsDTO(status="AVAILABLE", borrowerId=0,
                                       borrowerName="N/A", borrowedOn=None)
            else:
                dto = StatusDetailsDTO(
                    status=borrow_status_row.status,
                    borrowerId=borrower_row.id,
                    borrowerName=borrower_row.name,
                    borrowedOn=borrow_status_row.borrowed_on.strftime("%Y-%m-%d")
                )
            result.append((book, dto))
        return result

    def search_by_author_and_title(self, author: Optional[str], title: Optional[str]) -> list[Book]:
        query = self.db.query(Book)

        if author:
            query = query.filter(Book.author.ilike(f"%{author}%"))
        if title:
            query = query.filter(Book.title.ilike(f"%{title}%"))

        return query.all()

    def get_rented_books_report(self):
        now = datetime.utcnow()

        results = (
            self.db.query(
                Book.id.label("book_id"),
                Book.title.label("title"),
                BookBorrowStatus.borrowed_on.label("borrowed_on"),
                (func.julianday(func.now()) - func.julianday(BookBorrowStatus.borrowed_on)).label("days_rented")
            )
            .join(BookBorrowStatus, Book.id == BookBorrowStatus.book_id)
            .filter(BookBorrowStatus.status == "RENTED")
            .all()
        )
        return results
