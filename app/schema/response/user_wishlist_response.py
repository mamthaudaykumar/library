from pydantic import BaseModel, ConfigDict


class WishlistItemResponse(BaseModel):
    id: int
    user_id: int
    book_id: int

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
