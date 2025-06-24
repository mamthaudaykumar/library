import csv
from datetime import datetime

from fastapi.params import Depends, Path
from sqlalchemy.orm import Session
from pathlib import Path as FilePath

from config.cfg_sql_connection import get_db, SessionLocal
from app.repository.model import Book
from repository.model import UsersDetails, BookBorrowStatus


def _seed_books(db: Session, csv_path: Path) -> None:
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            book = Book(
                isbn=row["ISBN"],
                    book_id=row["Id"],
                title=row["Title"],
                author=row["Authors"],
                publication_year=int(row["Publication Year"]),
                language=row["Language"],
            )
            db.add(book)
    db.commit()

def _seed_user_data(db: Session, csv_path: Path) -> None:
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            users_details = UsersDetails( #id,name,email,phone,user_type
                id=row["id"],
                name=row["name"],
                email=row["email"],
                phone=row["phone"],
                user_type=row["user_type"],
            )
            db.add(users_details)
    db.commit()


def _seed_book_borrow_status_data(db: Session, csv_path: Path) -> None:
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            book_borrow_status = BookBorrowStatus(
                id=int(row["id"]),
                book_id=int(row["book_id"]),
                user_id=int(row["user_id"]),
                borrowed_on=datetime.fromisoformat(row["borrowed_on"]),
                due_date=datetime.fromisoformat(row["due_date"]) if row["due_date"] else None,
                status=row["status"],
                updated_on=datetime.fromisoformat(row["updated_on"]),
                created_on=datetime.fromisoformat(row["created_on"]),
            )
            db.add(book_borrow_status)
    db.commit()

def run_seed() -> None:
    with SessionLocal() as db:
        books_csv =  FilePath("resources/BackendSeedBookData.csv")
        if books_csv.exists():
            _seed_books(db, books_csv)

        user_data =  FilePath("resources/userSeedData.csv")
        if user_data.exists():
            _seed_user_data(db, user_data)

        borrow_data = FilePath("resources/book_rented_status.csv")
        if borrow_data.exists():
            _seed_book_borrow_status_data(db, borrow_data)