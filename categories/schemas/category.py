from pydantic import BaseModel


class CategoryListResponse(BaseModel):
    id: int
    name: str
    kind: str
