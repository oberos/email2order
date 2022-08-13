from pydantic import BaseModel
from typing import List


class OrderRow(BaseModel):
    item: str
    qty: str
    price: float = 0

class Order(BaseModel):
    """Pydantic model that represents customer order"""    
    company_number: str = '0'
    company_name: str = ''
    order_number: str = ''
    cust_ref: str = ''
    customer_order_date: str = '0'
    rows: List[OrderRow] = []
    error: str = ''
    error_description: str = ''
    comments: str = ''
