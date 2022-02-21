import csv
from .abstract import Exporter
import models


class Customer_aExporter(Exporter):
    def initialize_config(self, file_path: str):
        """A helper method used to store the column configuration.
        """
        self.file_path = file_path

    def extract_data(self) -> models.Order:
        """Class used to perform extraction from file

        Returns:
            Union[Order, List[Order]]: Depends of customer config returns pydantic Order class or list of that class.
        """
        customer_order = models.Order()
        with open(self.file_path, encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=';')
            for row in csv_reader:
                customer_order.company_name = 'Customer_a'
                customer_order.company_number = "100001"
                customer_order.order_number = row['col0']
                customer_order.cust_ref = row['col3']
                customer_order.customer_order_date = row['col1']
                order_row = models.OrderRow(
                    item=row['col15'],
                    qty=row['col16'],
                    price=float(row['col17'])
                )
                customer_order.rows.append(order_row)
        return customer_order