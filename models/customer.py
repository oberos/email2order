from pydantic import BaseModel, Field


class CustomerData(BaseModel):
    """Pydantic model that represents customer order data"""    
    name: str = Field(...,title='Customer Name', description='Customer name for order creation')
    filename: str = Field(...,title='Filename', description='Name of the file')
    contentBytes: str = Field(...,title='Attachment base64', description='File in base64 string')
