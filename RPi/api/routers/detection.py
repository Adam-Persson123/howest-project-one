from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_session
from models.detection import DetectionCreate, DetectionRead
from repositories.detection import DetectionRepository

router = APIRouter(prefix="/detection", tags=["Detections"])


def get_detection_repository(
    session: Annotated[Session, Depends(get_session)],
) -> DetectionRepository:
    return DetectionRepository(session)


@router.get("/", response_model=List[DetectionRead])
async def get_detections(repo: Annotated[DetectionRepository, Depends(get_detection_repository)]):
    '''
    Get all detections
    '''
    return repo.get_all()


@router.get("/class/{class_id}", response_model=List[DetectionRead])
async def get_detections_by_class(class_id: int, repo: Annotated[DetectionRepository, Depends(get_detection_repository)]):
    '''
    Get all detections for a given class
    '''
    return repo.get_by_class_id(class_id)


@router.get("/{id}", response_model=DetectionRead)
async def get_detection(id: int, repo: Annotated[DetectionRepository, Depends(get_detection_repository)]):
    '''
    Get a detection by id
    '''
    detection = repo.get_by_id(id)
    if not detection:
        raise HTTPException(status_code=404, detail=f"Detection {id} not found")
    return detection


@router.post("/", response_model=DetectionRead)
async def add_detection(
    detection: DetectionCreate,
    repo: Annotated[DetectionRepository, Depends(get_detection_repository)]
):
    '''
    Add a new detection
    '''
    return repo.insert(detection)


@router.delete("/{id}", response_model=DetectionRead)
async def delete_detection(
    id: int,
    repo: Annotated[DetectionRepository, Depends(get_detection_repository)]
):
    '''
    Delete a detection by id
    '''
    result = repo.delete_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Detection {id} not found")
    return result


@router.delete("/", response_model=List[DetectionRead])
async def delete_detections(repo: Annotated[DetectionRepository, Depends(get_detection_repository)]):
    '''
    Delete all detections
    '''
    result = repo.delete_all()
    if not result:
        raise HTTPException(status_code=404, detail="No detections found")
    return result


@router.put("/{id}", response_model=DetectionRead)
async def update_detection(
    id: int,
    detection: DetectionCreate,
    repo: Annotated[DetectionRepository, Depends(get_detection_repository)]
):
    '''
    Update a detection by id
    '''
    try:
        return repo.update(id, detection)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Detection {id} not found")