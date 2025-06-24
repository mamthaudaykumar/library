from fastapi import APIRouter, Depends, status

from app.service.user_wishlist_service import UserWishlistService
from app.schema.response.user_wishlist_response import WishlistItemResponse

router = APIRouter(
    prefix="/api/v1/user",
    tags=["User – Wishlist"],
)

@router.post(
    "/{user_id}/book/{book_id}/wishlist",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
    summary="Add a book to wishlist",
    operation_id="addToWishlist",
)
def add_wishlist_entry(
    user_id: int,
    book_id: int,
    service: UserWishlistService = Depends(),
):
    service.add(user_id, book_id)
    # 201 Created, no body needed
    return


@router.delete(
    "/{user_id}/book/{book_id}/wishlist",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    summary="Remove a book from wishlist",
    operation_id="removeFromWishlist",
)
def remove_wishlist_entry(
    user_id: int,
    book_id: int,
    service: UserWishlistService = Depends(),
):
    service.remove(user_id, book_id)
    # 204 No Content
    return


@router.get(
    "/{user_id}/wishlist",
    response_model=list[WishlistItemResponse],
    summary="List a user's wishlist",
    operation_id="listWishlist",
)
def list_wishlist(
    user_id: int,
    service: UserWishlistService = Depends(),
):
    # Convert ORM objects to DTOs if you have a response schema
    wishlist_rows = service.get_all(user_id)
    return [
        WishlistItemResponse.model_validate(row, from_attributes=True)
        for row in wishlist_rows
    ]
