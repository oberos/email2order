from pydantic import BaseModel


class SystemOrderResults(BaseModel):
    status_code: int
    error: str = ''
