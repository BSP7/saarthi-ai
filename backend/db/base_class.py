from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        # Simple snake case converter for BasicModel -> basic_model
        name = cls.__name__
        return "".join(["_" + i.lower() if i.isupper() else i for i in name]).lstrip("_") + "s"
