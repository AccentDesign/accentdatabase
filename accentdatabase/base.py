from sqlalchemy.orm import Mapped, as_declarative, declared_attr, mapped_column


@as_declarative()
class Base:
    """
    Base class all tables to inherit from
    https://docs.sqlalchemy.org/en/latest/orm/mapping_api.html#sqlalchemy.orm.declarative_base

    - example usage::

        from accentdatabase.base import Base

        class MyTable(Base)
            pass

    """

    @declared_attr
    def id(self) -> Mapped[int]:
        return mapped_column(primary_key=True)
