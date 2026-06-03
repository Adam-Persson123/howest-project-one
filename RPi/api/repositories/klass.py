from sqlmodel import Session, select
from models.klass import Class, ClassCreate

class ClassRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Class]:
        statement = select(Class)
        items = self.session.exec(statement).all()
        return items

    def get_by_id(self, class_id: int) -> Class:
        statement = select(Class).where(Class.id == class_id)
        item = self.session.exec(statement).first()
        return item

    def insert(self, payload: ClassCreate):
        item = Class.model_validate(payload)
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def delete_by_id(self, class_id: int):
        statement = select(Class).where(Class.id == class_id)
        existing_class = self.session.exec(statement).first()
        if existing_class:
            self.session.delete(existing_class)
            self.session.commit()
            return existing_class
        return None

    def update(self, class_id: int, payload: ClassCreate):
        klass = self.session.get(Class, class_id)
        if not klass:
            return None
        # Update all fields from payload
        for key, value in payload.model_dump().items():
            setattr(klass, key, value)
        self.session.commit()
        self.session.refresh(klass)
        return klass