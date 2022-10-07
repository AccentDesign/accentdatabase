from sqlalchemy import Column, String

from accentdatabase.base import Base
from accentdatabase.mixins import UUIDMixin


class Item(UUIDMixin, Base):
    __tablename__ = "items"

    name = Column(String(50), nullable=False, unique=True)
