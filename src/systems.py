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
        

class LocalSystem(System):
    def create_order(self, order_info: models.Order, customer_name: str) -> models.SystemOrderResults:
        if customer_name == 'Helion':
            return models.SystemOrderResults(status_code=501, error='Somesing is no yes')        
        else:
            return models.SystemOrderResults(status_code=201)        