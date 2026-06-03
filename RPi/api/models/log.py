from typing import Optional
from sqlmodel import Field, SQLModel

class LogBase(SQLModel):
    type: str
    log: str
    timestamp: str

class Log(LogBase, table=True):
    __tablename__ = "logs"
    id: Optional[int] = Field(default=None, primary_key=True)

class LogCreate(LogBase):
    pass

class LogRead(LogBase):
    id: int