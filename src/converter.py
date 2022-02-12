from . import customers
from .customers.abstract import Exporter
from .systems import System
from typing import Optional
import models


MAPPING = {
        "Helion": customers.HelionExtractor(),
        "Onepress": customers.OnepressExtractor()
    }

def read_exporter(customer_name: str) -> Optional[Exporter]:
    """Function used to choose proper customer extractor based on name

    Args:
        customer_name (str): Customer name

    Returns:
        Optional[Exporter]: customer exporter class. None if customer not found
    """
    if customer_name in MAPPING:
        return MAPPING[customer_name]
    return None
    

class Extractor():
    """Class used to convert post request to order in choosed system"""

    def __init__(self, customer_data_model: models.CustomerData, system: System):
        """Class used to convert email to order in choosed system (OrderCreator)

        Args:
            model (models.CustomerData): Pydantic model with API data
            system (System): Desired system where order will be created
        """
        self.customer_data_model = customer_data_model
        self.temp_file_name = ''
        self.system = system

    def process_order(self) -> models.ConversionResults:
        exporter = read_exporter(self.customer_data_model.name)
        if exporter is None:
            return models.ConversionResults(message="Customer not supported.")
        exporter.initialize_config('mock_path', 'mock subject')
        extracted_order_data = exporter.extract_data()
        results = self.system.create_order(extracted_order_data, self.customer_data_model.name)
        if results.status_code != 201:
            return models.ConversionResults(message=f'Order not created due to error: {results.error}') 
        return models.ConversionResults(message='Order created', success=True) 
        
