import os
from fastapi import FastAPI, Response, status
import models
from src.systems import LocalSystem
from src.extractor import Converter
from src.extractor import MAPPING
from src.systems import LOCAL_SYSTEM_DATABASE


app = FastAPI()

@app.get("/orders", tags=["Orders"])
async def orders():
    """Get all customer orders"""    
    return LOCAL_SYSTEM_DATABASE

@app.get("/customers", tags=["Customers"])
async def customers():
    """Get all supported customers"""    
    return MAPPING

@app.post("/create_order", status_code=status.HTTP_201_CREATED, tags=["integration"])
def create_order_for_customer(customer_data_model: models.CustomerData, response: Response):
    """Create order in database for customer"""
    creator = LocalSystem()
    extractor_object = Converter(customer_data_model, creator)
    result = extractor_object.process_order()
    if result.success is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return result

# Uvicorn config
if __name__ == "__main__":  # pragma: no cover
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8200, reload=True, debug=True, log_config='logging.yaml')