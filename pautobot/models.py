from pydantic import BaseModel


class Query(BaseModel):
    mode: str
    query: str
