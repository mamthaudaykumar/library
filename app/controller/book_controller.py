from fastapi import APIRouter, Depends, Query, status
from typing import List, Literal, Optional

from app.schema.request.book_request import BookRequest
from app.schema.response.book_response import BookResponse, BookCreateResponse
from app.service.book_service import BookService
from app.schema.request.book_borrow_status import BookBorrowStatusRequest
from app.schema.response.book_response import BookUpdateResponse

router = APIRouter(prefix="/api/v1/book", tags=["Book"])

@router.post("/", response_model=BookCreateResponse, status_code=status.HTTP_201_CREATED,
             summary="Create books",
    operation_id="createBooks")
def create_book(book: BookRequest, book_service: BookService = Depends()):
    return book_service.create(book)

@router.put("/{book_id}", response_model=BookUpdateResponse)
def update_book(book_id: int, updated_book: BookRequest, book_service: BookService = Depends()):
    return book_service.update(book_id, updated_book)

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, book_service: BookService = Depends()):
    return book_service.get_one(book_id)

#Pagination should be added not added here, no time
@router.get("/", response_model=List[BookResponse])
def get_all_books(book_service: BookService = Depends()):
    return book_service.get_all()

#URI can be better - i did it for quick proceeding as fast api was haivng issues
@router.put(
    "/bookstatus/update",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update book status",
    operation_id="update_book_status",
)
def update_book_status(
    book_id: int,
    req: BookBorrowStatusRequest,
    book_service: BookService = Depends(),
):
    book_service.update_status(req)


@router.get("/books/search", response_model=List[BookResponse], summary="Search books by author and/or title")
def search_books(
    author: Optional[str] = Query(None, description="Filter by author name"),
    title: Optional[str] = Query(None, description="Filter by book title"),
        book_service: BookService = Depends(),
):
    return book_service.search(author=author, title=title)


@router.get(
    "/report/rented-books",
    summary="Get report of currently rented books and rental duration",
    operation_id="getRentedBooksReport"
)
def rented_books_report(service: BookService = Depends()):
    return service.get_rental_report()

