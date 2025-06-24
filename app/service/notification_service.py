
from app.service.user_wishlist_service import UserWishlistService


class NotificationService:
    def __init__(self):
        self.wishlidt_service = UserWishlistService()

    async def notify(self):
        wishlist_items = self.wishlidt_service.get_all()

        for item in wishlist_items:
            print(f"Book {item.book_id} available")  # or use logging / push notification
