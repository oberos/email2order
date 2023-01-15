from fastapi import FastAPI, Response, status
import models
from typing import List
from src.systems import LocalSystem, RemoteSystem
from src.extractor import Converter
from src.extractor import MAPPING

app = FastAPI()


@app.get("/customers", tags=["Customers"])
async def customers():
    """Get all supported customers"""
    return MAPPING


@app.get("/orders", tags=["Orders"], response_model=List[models.Order])
async def get_orders(remote_system: bool = False):
    """Get all customer orders"""
    if remote_system is True:
        return RemoteSystem().get_all_orders()
    return LocalSystem().get_all_orders()


@app.post("/orders", status_code=status.HTTP_201_CREATED, tags=["Orders"])
def create_order_for_customer(customer_data_model: models.CustomerData, response: Response, remote_system: bool = False):
    """Create order in database for customer"""
    creator = LocalSystem()
    if remote_system is True:
        creator = RemoteSystem()
    extractor_object = Converter(customer_data_model, creator)
    result = extractor_object.process_order()
    if result.success is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return result


# Uvicorn config
if __name__ == "__main__":  # pragma: no cover
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8200, reload=True, debug=True, log_config='logging.yaml')
