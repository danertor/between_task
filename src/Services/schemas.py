from pydantic import BaseModel


class ApiServiceRow(BaseModel):
    userId: int
    id: int
    title: str
    completed: bool = False
