from sqlmodel import Session, select
from models.detection import Detection, DetectionCreate


class DetectionRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Detection]:
        statement = select(Detection)
        items = self.session.exec(statement).all()
        return items

    def get_by_id(self, detection_id: int) -> Detection:
        statement = select(Detection).where(Detection.id == detection_id)
        item = self.session.exec(statement).first()
        return item

    def get_by_class_id(self, class_id: int) -> list[Detection]:
        statement = select(Detection).where(Detection.class_id == class_id)
        items = self.session.exec(statement).all()
        return items

    def insert(self, payload: DetectionCreate) -> Detection:
        item = Detection.model_validate(payload)
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def delete_by_id(self, detection_id: int) -> Detection | None:
        statement = select(Detection).where(Detection.id == detection_id)
        existing = self.session.exec(statement).first()
        if existing:
            self.session.delete(existing)
            self.session.commit()
            return existing
        return None

    def delete_all(self) -> list[Detection]:
        statement = select(Detection)
        items = self.session.exec(statement).all()
        for item in items:
            self.session.delete(item)
        self.session.commit()
        return items

    def update(self, detection_id: int, payload: DetectionCreate) -> Detection:
        detection = self.session.get(Detection, detection_id)
        if not detection:
            raise ValueError(f"Detection with id {detection_id} does not exist")
        for key, value in payload.model_dump().items():
            setattr(detection, key, value)
        self.session.commit()
        self.session.refresh(detection)
        return detection