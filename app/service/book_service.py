# app/service/book_service.py
from typing import List, Literal, Optional, Dict
from fastapi import Depends, HTTPException
from app.repository.dao.book_dao import BookDAO
from app.schema.request.book_request import BookRequest
from app.schema.response.book_response import BookResponse, BookCreateResponse, BookUpdateResponse
from app.repository.model.book import Book
from config.dependencies import get_book_dao
from app.repository.model import BookBorrowStatus
from schema.request.book_borrow_status import BookBorrowStatusRequest
from schema.response.book_response import StatusDetails
from app.service.notification_service import NotificationService


class BookService:
    def __init__(self, book_dao: BookDAO = Depends(get_book_dao)
                 , notification_service: NotificationService = Depends()):
        self.book_dao = book_dao
        self.notification_service = notification_service

    def create(self, book_req: BookRequest) -> BookCreateResponse:
        db_book = Book(**book_req.model_dump())
        created = self.book_dao.create(db_book)
        return BookCreateResponse.from_orm(created)

    def update(self, book_id: int, updated: BookRequest) -> BookResponse:
        db_book = Book(**updated.model_dump())
        book = self.book_dao.update(book_id, db_book)
        return BookUpdateResponse.from_orm(book)

    def get_one(self, book_id: int) -> BookResponse:
        book = self.book_dao.get_one(book_id)
        res = BookResponse.from_orm(book);
        status_details = self.book_dao.get_book_status_details("RENTED", book_id);
        res.status_details = StatusDetails(**status_details.model_dump())
        return res

    def get_all(self) -> List[BookResponse]:
        rows = self.book_dao.get_all_with_status(borrow_status="RENTED")
        responses: list[BookResponse] = []

        for book, status_dto in rows:
            resp = BookResponse.from_orm(book)
            resp.status_details = StatusDetails.model_validate(status_dto)  # ✔ safe conversion
            responses.append(resp)

        return responses

    def update_status(self, req: BookBorrowStatusRequest) -> dict:
        #TODO userId exist check, book exist check
        self.book_dao.update_status(req)
        if(req.status == "RETURNED"):
            # pass
            self.notification_service.notify()
        return {
            "message": "Status updated",
            "book_id": req.book_id,
            "new_status": req.status,
        }

    def search(self, author: Optional[str] = None, title: Optional[str] = None) -> List[BookResponse]:
        books = self.book_dao.search_by_author_and_title(author=author, title=title)

        responses = [BookResponse.from_orm(book) for book in books]
        return responses

    def get_rental_report(self) -> List[Dict]:
        rented_books = self.book_dao.get_rented_books_report()

        return [
            {
                "book_id": row.book_id,
                "title": row.title,
                "borrowed_on": row.borrowed_on,
                "days_rented": int(row.days_rented),
            }
            for row in rented_books
        ]