from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from accentdatabase.base import Base
from accentdatabase.mixins import UUIDMixin


class Item(UUIDMixin, Base):
    __tablename__ = "items"

    name: Mapped[str] = mapped_column(String(50), unique=True)
