from typing import Optional
from sqlmodel import Field, SQLModel

class ClassBase(SQLModel):
    name: str
    description: str

class Class(ClassBase, table=True):
    __tablename__ = "classes"
    id: Optional[int] = Field(default=None, primary_key=True)

class ClassCreate(ClassBase):
    pass

class ClassRead(ClassBase):
    id: int