from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.database.connection import get_session
from app.services.category_service import CategoryServiceInterface
from app.services.instances import get_category_service, get_news_page_service
from app.services.news_page_service import NewsPageServiceInterface

SessionDep = Annotated[Session, Depends(get_session)]
CategoryServiceDep = Annotated[CategoryServiceInterface, Depends(get_category_service)]
NewsPageServiceDep = Annotated[NewsPageServiceInterface, Depends(get_news_page_service)]
