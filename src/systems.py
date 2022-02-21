from abc import ABC, abstractmethod
import models


class System(ABC):
    @abstractmethod
    def create_order(self, order_info: models.Order, customer_name: str) -> models.SystemOrderResults:
        """Creates order in desired system

        Args:
            order_info (models.Order): Model with order data
            customer_config (models.Customer): Model with customer configuration from db

        Returns:
            models.SystemOrderResults: Model with order creation results
        """        


LOCAL_SYSTEM_DATABASE = []

class LocalSystem(System):
    def create_order(self, order_info: models.Order, customer_name: str) -> models.SystemOrderResults:
        if customer_name == 'Customer_a':
            return models.SystemOrderResults(status_code=501, error='Somesing is no yes')        
        else:            
            order_row = {
                "id": len(LOCAL_SYSTEM_DATABASE) + 1,
                "details": order_info.dict()
            }
            LOCAL_SYSTEM_DATABASE.append(order_row)
            return models.SystemOrderResults(status_code=201)        