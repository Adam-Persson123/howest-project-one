from sqlmodel import Session as DBSession, select
from models.session import Session, SessionCreate

class SessionRepository:
    def __init__(self, session: DBSession):
        self.session = session

    def get_all(self) -> list[Session]:
        statement = select(Session)
        items = self.session.exec(statement).all()
        return items

    def get_by_id(self, session_id: int) -> Session:
        statement = select(Session).where(Session.id == session_id)
        item = self.session.exec(statement).first()
        return item

    def insert(self, payload: SessionCreate) -> Session:
        item = Session.model_validate(payload)
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def delete_by_id(self, session_id: int) -> Session | None:
        statement = select(Session).where(Session.id == session_id)
        existing = self.session.exec(statement).first()
        if existing:
            self.session.delete(existing)
            self.session.commit()
            return existing
        return None

    def delete_all(self) -> list[Session]:
        statement = select(Session)
        items = self.session.exec(statement).all()
        for item in items:
            self.session.delete(item)
        self.session.commit()
        return items

    def update(self, session_id: int, payload: SessionCreate) -> Session:
        session = self.session.get(Session, session_id)
        if not session:
            raise ValueError(f"Session with id {session_id} does not exist")
        for key, value in payload.model_dump().items():
            setattr(session, key, value)
        self.session.commit()
        self.session.refresh(session)
        return session