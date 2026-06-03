from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_session
from models.log import LogCreate, LogRead
from repositories.log import LogRepository

router = APIRouter(prefix="/log", tags=["Logs"])


def get_log_repository(
    session: Annotated[Session, Depends(get_session)],
) -> LogRepository:
    return LogRepository(session)


@router.get("/", response_model=List[LogRead])
async def get_logs(repo: Annotated[LogRepository, Depends(get_log_repository)]):
    '''
    Get all logs
    '''
    return repo.get_all()


@router.get("/type/{type}", response_model=List[LogRead])
async def get_logs_by_type(type: str, repo: Annotated[LogRepository, Depends(get_log_repository)]):
    '''
    Get all logs of a given type
    '''
    return repo.get_by_type(type)
    
    
@router.get("/{id}", response_model=LogRead)
async def get_log(id: int, repo: Annotated[LogRepository, Depends(get_log_repository)]):
    '''
    Get a log by id
    '''
    log = repo.get_by_id(id)
    if not log:
        raise HTTPException(status_code=404, detail=f"Log {id} not found")
    return log


@router.post("/", response_model=LogRead)
async def add_log(
    log: LogCreate,
    repo: Annotated[LogRepository, Depends(get_log_repository)]
):
    '''
    Add a new log
    '''
    return repo.insert(log)


@router.delete("/{id}", response_model=LogRead)
async def delete_log(
    id: int,
    repo: Annotated[LogRepository, Depends(get_log_repository)]
):
    '''
    Delete a log by id
    '''
    result = repo.delete_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Log {id} not found")
    return result


@router.put("/{id}", response_model=LogRead)
async def update_log(
    id: int,
    log: LogCreate,
    repo: Annotated[LogRepository, Depends(get_log_repository)]
):
    '''
    Update a log by id
    '''
    try:
        return repo.update(id, log)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Log {id} not found")