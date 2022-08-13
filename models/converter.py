from pydantic import BaseModel


class ConversionResults(BaseModel):
    success: bool = False
    message: str = 'Error'