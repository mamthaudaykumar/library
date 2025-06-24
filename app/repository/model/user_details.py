
from sqlalchemy.orm import Mapped, mapped_column

from app.repository.model import Base

class UsersDetails( Base):
    __tablename__ = "users_details"

    id:    Mapped[int] = mapped_column(primary_key=True)
    name:  Mapped[str]
    email: Mapped[str]
    phone: Mapped[str]
    user_type: Mapped[str] #admin or user