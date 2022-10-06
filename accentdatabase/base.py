from sqlalchemy import Column, Integer
from sqlalchemy.orm import as_declarative, declared_attr


@as_declarative()
class Base:
    @declared_attr
    def id(self):
        return Column(Integer, primary_key=True)
