from fastapi import HTTPException, status
from fastapi.params import Depends

from app.repository.dao.user_wishlist_dao import UserWishlistDAO
from config.cfg_sql_connection import get_db


class UserWishlistService:
    def __init__(self, db=Depends(get_db)):
        self.dao = UserWishlistDAO(db)

    def add(self, user_id: int, book_id: int) -> None:
        if self.dao.is_in_wishlist(user_id, book_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Book already in wishlist",
            )
        self.dao.add_to_wishlist(user_id, book_id)

    def remove(self, user_id: int, book_id: int) -> None:
        removed = self.dao.remove_from_wishlist(user_id, book_id)
        if not removed:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wishlist entry not found",
            )

    def get_all(self, user_id: int):
        return self.dao.get_wishlist_by_user(user_id)

    def get_all_wishlist(self):
        return self.dao.get_all_wishlist()
