from typing import Optional
from sqlmodel import Field, SQLModel

class DetectionBase(SQLModel):
    confidence: float
    timestamp: str

class Detection(DetectionBase, table=True):
    __tablename__ = "detections"
    id: Optional[int] = Field(default=None, primary_key=True)
    class_id: int = Field(foreign_key="classes.id")

class DetectionCreate(DetectionBase):
    class_id: int

class DetectionRead(DetectionBase):
    id: int
    class_id: int