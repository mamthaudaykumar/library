from pydantic import BaseModel, Field, StrictInt, StrictStr

class BookRequest(BaseModel):
    book_id: StrictInt = Field(...)
    isbn: StrictStr = Field(...)
    author: StrictStr = Field(...)
    publication_year: StrictInt = Field(..., ge=0)
    title: StrictStr = Field(...)
    language: StrictStr = Field(...)

    class Config:
        orm_mode = True