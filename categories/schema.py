from pydantic import BaseModel

from utils.choices.choice import CategoryKindChoices


class CategoryListOutput(BaseModel):
    id: int
    name: str
    kind: CategoryKindChoices
