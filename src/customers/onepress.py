from .abstract import Exporter
import models


class OnepressExtractor(Exporter):
    def initialize_config(self, file_path: str, email_subject: str = None):
        """A helper method used to store the column configuration.
        """
        self.file_path = file_path
        self.email_subject = email_subject

    def extract_data(self) -> models.Order:
        """Class used to perform extraction from file

        Returns:
            Union[Order, List[Order]]: Depends of customer config returns pydantic Order class or list of that class.
        """
        return models.Order()