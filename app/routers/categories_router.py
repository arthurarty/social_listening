from typing import Annotated, List

from fastapi import APIRouter, Query, status

from app.database.models.categories import Category
from app.dependencies import CategoryServiceDep, SessionDep
from app.schemas.category_schema import CategoryCreate, CategoryRead

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryCreate,
    session: SessionDep,
    category_service: CategoryServiceDep,
):
    """
    Creates a category, or updates it if a category with the same name
    already exists
    """
    category_id = category_service.store_category(
        session, Category(**category.model_dump())
    )
    return {"id": category_id}


@router.get("/", response_model=List[CategoryRead])
def list_categories(
    session: SessionDep,
    category_service: CategoryServiceDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    """
    Lists categories
    """
    return category_service.get_categories(session, skip=skip, limit=limit)
