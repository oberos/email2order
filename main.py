from fastapi import FastAPI, Response, status
import models
from src.systems import LocalSystem
from src.converter import Extractor
from src.converter import MAPPING


app = FastAPI()


@app.get("/customers", tags=["Customers"])
async def customers():
    """Get all supported customers"""    
    return MAPPING

@app.post("/create_order", status_code=status.HTTP_201_CREATED, tags=["integration"])
def create_order_for_customer(customer_data_model: models.CustomerData, response: Response):
    """Create order in database for customer  
    More info in Schema below
    """
    creator = LocalSystem()
    extractor_object = Extractor(customer_data_model, creator)
    result = extractor_object.process_order()
    if result.success is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return result


