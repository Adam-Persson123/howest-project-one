from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_session
from models.klass import ClassCreate, ClassRead
from repositories.klass import ClassRepository

router = APIRouter(prefix="/class", tags=['Classes'])

def get_class_repository(
    session: Annotated[Session, Depends(get_session)],
) -> ClassRepository:
    return ClassRepository(session)

@router.get("/", response_model=List[ClassRead])
async def get_classes(repo: Annotated[ClassRepository, Depends(get_class_repository)]):
    '''
    Get all classes
    '''
    return repo.get_all()

@router.get("/{id}", response_model=ClassRead)
async def get_class(id: int, repo: Annotated[ClassRepository, Depends(get_class_repository)]):
    '''
    Get a class by id
    '''
    klass = repo.get_by_id(id)
    if not klass:
        raise HTTPException(status_code=404, detail=f"Class {id} not found")
    return klass

@router.post("/", response_model=ClassRead)
async def add_class(
    klass: ClassCreate,
    repo: Annotated[ClassRepository, Depends(get_class_repository)]
):
    '''
    Add a new class
    '''
    return repo.insert(klass)

@router.delete("/{id}", response_model=ClassRead)
async def delete_class(
    id: int,
    repo: Annotated[ClassRepository, Depends(get_class_repository)]
):
    '''
    Delete a class
    '''
    result = repo.delete_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Class {id} not found")
    return result

@router.put("/{id}", response_model=ClassRead)
async def update_class(
    id: int,
    klass: ClassCreate,
    repo: Annotated[ClassRepository, Depends(get_class_repository)]
):
    '''
    Update a class
    '''
    try:
        return repo.update(id, klass)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Class {id} not found")