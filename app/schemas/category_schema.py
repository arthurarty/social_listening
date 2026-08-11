from pydantic import BaseModel


class CategoryCreate(BaseModel):
    """
    Schema for request to create a category
    """

    name: str
    description: str
    examples: str


class CategoryRead(BaseModel):
    """
    Schema for returning a category
    """

    id: int
    name: str
    description: str
    examples: str

    class Config:
        from_attributes = True
