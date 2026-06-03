from typing import Optional
from sqlmodel import Field, SQLModel

class SessionBase(SQLModel):
    time_from: str
    time_to: str

class Session(SessionBase, table=True):
    __tablename__ = "sessions"
    id: Optional[int] = Field(default=None, primary_key=True)

class SessionCreate(SessionBase):
    pass

class SessionRead(SessionBase):
    id: int