from abc import ABC, abstractmethod
from typing import List, Union
from models import Order


class Exporter(ABC):
    @abstractmethod
    def initialize_config(self, file_path: str, email_subject: str):
        """Class used to initialize configuration for exporter

        Args:
            file_path (str): Temporary file path for extracting
            email_subject (str): subject of email
        """

    @abstractmethod
    def extract_data(self) -> Order:
        """Class used to perform extraction from file

        Returns:
            Order: Returns pydantic Order class.
        """   
