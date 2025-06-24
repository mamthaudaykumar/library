from sqlalchemy.orm import Session
from app.repository.model.user_book_wishlist import UserBookWishlist


class UserWishlistDAO:
    def __init__(self, db: Session):
        self.db = db

    def add_to_wishlist(self, user_id: int, book_id: int) -> UserBookWishlist:
        wishlist_item = UserBookWishlist(user_id=user_id, book_id=book_id)
        self.db.add(wishlist_item)
        self.db.commit()
        self.db.refresh(wishlist_item)
        return wishlist_item

    def get_wishlist_by_user(self, user_id: int) -> list[UserBookWishlist]:
        return (
            self.db.query(UserBookWishlist)
            .filter(UserBookWishlist.user_id == user_id)
            .all()
        )

    def get_all_wishlist(self) -> list[UserBookWishlist]:
        return (
            self.db.query(UserBookWishlist)
            .all()
        )

    def remove_from_wishlist(self, user_id: int, book_id: int) -> bool:
        item = (
            self.db.query(UserBookWishlist)
            .filter(
                UserBookWishlist.user_id == user_id,
                UserBookWishlist.book_id == book_id,
            )
            .first()
        )
        if item:
            self.db.delete(item)
            self.db.commit()
            return True
        return False

    def is_in_wishlist(self, user_id: int, book_id: int) -> bool:
        return (
            self.db.query(UserBookWishlist)
            .filter(
                UserBookWishlist.user_id == user_id,
                UserBookWishlist.book_id == book_id,
            )
            .first()
            is not None
        )
