from . import customers
from .customers.abstract import Exporter
from .systems import System
from .file_handler import FileHandler
from typing import Optional
import models


MAPPING = {
        "Customer_a": customers.CustomerAExporter(),
        "Customer_b": customers.CustomerBExporter()
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
    

class Converter():
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
        file_object = FileHandler(self.customer_data_model.contentBytes, self.customer_data_model.filename)
        file_path = file_object.save_base64_file()
        if file_path.startswith('Error'):
            return models.ConversionResults(message=file_path)
        exporter.initialize_config(file_path)
        extracted_order_data = exporter.extract_data()
        file_object.delete_old_files()
        if extracted_order_data.error != '':
            return models.ConversionResults(message=f"Problem with extracting data from file.\n Details: {extracted_order_data.error_description}")
        results = self.system.create_order(extracted_order_data, self.customer_data_model.name)
        if results.status_code != 201:
            return models.ConversionResults(message=f'Order not created due to error: {results.error}') 
        return models.ConversionResults(message='Order created', success=True) 
        
