from pydantic import BaseModel, Field, ConfigDict, StrictStr, conint

class BookBorrowStatusRequest(BaseModel):
    user_id: conint(strict=True) = Field(..., description="ID of the user borrowing the book")
    book_id: conint(strict=True) = Field(..., description="ID of the book being borrowed")
    status: StrictStr = Field(..., description="Borrow status. RENTED/RETURNED")

    model_config = ConfigDict(from_attributes=True)

