from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ---------- nested DTO -------------------------------------------------
class StatusDetails(BaseModel):
    status: str
    borrower_id: Optional[int] = Field(alias="borrowerId", default=None)
    borrower_name: Optional[str] = Field(alias="borrowerName", default=None)
    borrowed_on: Optional[datetime] = Field(alias="borrowedOn", default=None)

    model_config = ConfigDict(
        from_attributes=True,      # allow .from_orm()
        populate_by_name=True      # accept/emit camelCase aliases in JSON
    )


# ---------- base class for book‑like responses -------------------------
class _BookBase(BaseModel):
    id: int
    book_id: int
    isbn: str
    author: str
    publication_year: Optional[int] = None
    title: str
    language: Optional[str] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


# ---------- concrete response DTOs -------------------------------------
class BookResponse(_BookBase):
    status_details: Optional[StatusDetails] = None


class BookCreateResponse(_BookBase):
    """Returned right after a book is created."""
    # no extra fields


class BookUpdateResponse(_BookBase):
    """Returned after a book is updated."""
    # no extra fields
