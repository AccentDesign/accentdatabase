from sqlalchemy import Column, String

from accentdatabase import Base


class Item(Base):
    __tablename__ = "items"

    name = Column(String(50), nullable=False, unique=True)
