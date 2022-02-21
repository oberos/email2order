from bs4 import BeautifulSoup
from bs4.element import Tag
from typing import List, Optional
from .abstract import Exporter
import models


class Customer_bExporter(Exporter):
    def initialize_config(self, file_path: str):
        """A helper method used to store the column configuration.
        """
        self.file_path = file_path

    def _get_data(self, tag2check: Tag, list2check: List[str]) -> Optional[str]:
        """Helper method for getting nested tag from html/xml tree.  
        Prevents code to fail if one of tags is not found.

        Args:
            tag2check (Tag): Tag where initial search needs to be performed
            list2check (List[str]): List of tag names to check in tree

        Returns:
            Optional[str]: Bottom tag text or None if not found

        Example:
            top_tag = <tag1>
                        <tag2>
                            <tag3>
                                <tag4>Some_value</tag4>
                            </tag3>
                        </tag2>
                    </tag1>
            result = self._get_data(top_tag, ["tag1","tag2","tag3","tag4"])
            assert result == 'Some_value'
        """        
              
        last_result = ""
        for item in list2check:
            if last_result == '':
                current_check = tag2check.find(item)
            elif last_result is None:
                return None
            else:
                current_check = last_result.find(item)
            if isinstance(current_check, Tag):
                last_result = current_check
            else:
                last_result = None
        return last_result.text if last_result else None

    def extract_data(self) -> models.Order:
        """Class used to perform extraction from file

        Returns:
            Union[Order, List[Order]]: Depends of customer config returns pydantic Order class or list of that class.
        """
        customer_order = models.Order()
        with open(self.file_path, "r", encoding='utf-8') as infile:
            contents = infile.read()
        soup = BeautifulSoup(contents, 'xml')
        order_header = soup.find("OrderHeader")
        order_lines = soup.find("OrderLines")
        if not isinstance(order_header, Tag) or not isinstance(order_lines, Tag):
            customer_order.error = 'File Error'
            customer_order.error_description = 'Problem with fetching data from XML file'
            return customer_order
        customer_order.company_name = 'Customer_b'
        customer_order.company_number = '100002'
        customer_order.order_number = self._get_data(order_header, ['PurchaseOrder', 'Number']) or ''
        customer_order.customer_order_date = self._get_data(order_header, ['PurchaseOrder', 'Date']) or ''
        customer_order.cust_ref = self._get_data(order_header, ['Reference', 'Name']) or ''
        for item in order_lines.findAll("Line"):
            line_item_number = self._get_data(item, ['RequestedItem', 'Number']) or ''
            line_item_quantity = self._get_data(item, ['RequestedItem', 'Quantity']) or ''
            line_item_price = self._get_data(item, ['RequestedItem', 'PurchasePrice']) or 0
            if line_item_number == '' or line_item_quantity == '':
                customer_order.comments += '\nRow not created due to problems with fetching item number or quantity from file'
                continue
            order_row = models.OrderRow(
                    item=line_item_number,
                    qty=line_item_quantity,
                    price=float(line_item_price)
                )
            customer_order.rows.append(order_row)
        return customer_order