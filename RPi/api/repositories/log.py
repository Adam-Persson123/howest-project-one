from sqlmodel import Session, select
from models.log import Log, LogCreate


class LogRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Log]:
        statement = select(Log)
        items = self.session.exec(statement).all()
        return items

    def get_by_id(self, log_id: int) -> Log:
        statement = select(Log).where(Log.id == log_id)
        item = self.session.exec(statement).first()
        return item

    def get_by_type(self, type: str) -> list[Log]:
        statement = select(Log).where(Log.type == type)
        items = self.session.exec(statement).all()
        return items

    def insert(self, payload: LogCreate) -> Log:
        item = Log.model_validate(payload)
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def delete_by_id(self, log_id: int) -> Log | None:
        statement = select(Log).where(Log.id == log_id)
        existing = self.session.exec(statement).first()
        if existing:
            self.session.delete(existing)
            self.session.commit()
            return existing
        return None

    def update(self, log_id: int, payload: LogCreate) -> Log:
        log = self.session.get(Log, log_id)
        if not log:
            raise ValueError(f"Log with id {log_id} does not exist")
        for key, value in payload.model_dump().items():
            setattr(log, key, value)
        self.session.commit()
        self.session.refresh(log)
        return log