from typing import Annotated, List

from fastapi import APIRouter, Query, status

from app.database.models.topics import Topic
from app.dependencies import SessionDep, TopicServiceDep
from app.schemas.topic_schema import TopicCreate, TopicRead

router = APIRouter(prefix="/topics", tags=["topics"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_topic(
    topic: TopicCreate,
    session: SessionDep,
    topic_service: TopicServiceDep,
):
    """
    Creates a topic, or updates it if a topic with the same name
    already exists
    """
    topic_id = topic_service.store_topic(session, Topic(**topic.model_dump()))
    return {"id": topic_id}


@router.get("/", response_model=List[TopicRead])
def list_topics(
    session: SessionDep,
    topic_service: TopicServiceDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    """
    Lists topics
    """
    return topic_service.get_topics(session, skip=skip, limit=limit)
