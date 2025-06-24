import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import your ORM models and DAO/service layers
from app.repository.model.book import Book
from app.repository.dao.book_dao import BookDAO
from app.service.book_service import BookService
from app.repository.model import BookBorrowStatus


class DummyNotificationService:
    """A stand‑in for NotificationService so tests stay fast and isolated."""

    def notify(self):
        pass


@pytest.fixture()
def db_session():
    """Create a fresh in‑memory SQLite DB for every test function."""

    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(bind=engine)

    # Build tables from the metadata shared by your models
    Book.metadata.create_all(engine)

    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def populated_db(db_session):
    """Insert two books (both currently RENTED) so tests have predictable data."""

    now = datetime.utcnow()

    # Two sample books
    book_hp = Book(
        id=1,
        isbn="111",
        author="J.K. Rowling",
        publication_year=1997,
        title="Harry Potter",
        language="EN",
    )
    book_habits = Book(
        id=2,
        isbn="222",
        author="James Clear",
        publication_year=2018,
        title="Atomic Habits",
        language="EN",
    )
    db_session.add_all([book_hp, book_habits])
    db_session.flush()  # assign PKs if not set manually

    # Their rental status rows (5 and 2 days ago)
    status_hp = BookBorrowStatus(
        book_id=book_hp.id,
        user_id=1,
        borrowed_on=now - timedelta(days=5),
        due_date=None,
        status="RENTED",
        created_on=now,
        updated_on=now,
    )
    status_habits = BookBorrowStatus(
        book_id=book_habits.id,
        user_id=2,
        borrowed_on=now - timedelta(days=2),
        due_date=None,
        status="RENTED",
        created_on=now,
        updated_on=now,
    )

    db_session.add_all([status_hp, status_habits])
    db_session.commit()

    return db_session


def test_search_by_author(populated_db):
    """BookService.search should filter by author (case‑insensitive substring)."""

    dao = BookDAO(populated_db)
    service = BookService(book_dao=dao, notification_service=DummyNotificationService())

    results = service.search(author="rowling")

    assert len(results) == 1
    assert results[0].author == "J.K. Rowling"
    assert results[0].title == "Harry Potter"


def test_rented_books_report_days(populated_db):
    """DAO should calculate integer day deltas correctly using SQLite julianday()."""

    dao = BookDAO(populated_db)
    rows = dao.get_rented_books_report()

    # Extract and round to whole days for robustness
    actual_days = sorted(int(round(row.days_rented)) for row in rows)

    assert actual_days == [2, 5]
