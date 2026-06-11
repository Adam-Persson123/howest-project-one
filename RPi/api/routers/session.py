from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session as DBSession
from database import get_session
from models.session import SessionCreate, SessionRead
from repositories.session import SessionRepository

router = APIRouter(prefix="/session", tags=["Sessions"])


def get_session_repository(
    session: Annotated[DBSession, Depends(get_session)],
) -> SessionRepository:
    return SessionRepository(session)


@router.get("/", response_model=List[SessionRead])
async def get_sessions(repo: Annotated[SessionRepository, Depends(get_session_repository)]):
    '''
    Get all sessions
    '''
    return repo.get_all()


@router.get("/{id}", response_model=SessionRead)
async def get_session(id: int, repo: Annotated[SessionRepository, Depends(get_session_repository)]):
    '''
    Get a session by id
    '''
    session = repo.get_by_id(id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session {id} not found")
    return session


@router.post("/", response_model=SessionRead)
async def add_session(
    session: SessionCreate,
    repo: Annotated[SessionRepository, Depends(get_session_repository)]
):
    '''
    Add a new session
    '''
    return repo.insert(session)


@router.delete("/{id}", response_model=SessionRead)
async def delete_session(
    id: int,
    repo: Annotated[SessionRepository, Depends(get_session_repository)]
):
    '''
    Delete a session by id
    '''
    result = repo.delete_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Session {id} not found")
    return result


@router.delete("/", response_model=List[SessionRead])
async def delete_sessions(repo: Annotated[SessionRepository, Depends(get_session_repository)]):
    '''
    Delete all sessions
    '''
    result = repo.delete_all()
    if not result:
        raise HTTPException(status_code=404, detail="No sessions found")
    return result


@router.put("/{id}", response_model=SessionRead)
async def update_session(
    id: int,
    session: SessionCreate,
    repo: Annotated[SessionRepository, Depends(get_session_repository)]
):
    '''
    Update a session by id
    '''
    try:
        return repo.update(id, session)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Session {id} not found")