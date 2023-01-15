import os
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from pymongo import MongoClient
import models


class AbstractSystem(ABC):
    @abstractmethod
    def create_order(self, order_info: models.Order) -> models.SystemOrderResults:
        """Creates order in desired system

        Args:
            order_info (models.Order): Model with order data

        Returns:
            models.SystemOrderResults: Model with order creation results
        """

    @abstractmethod
    def get_all_orders(self) -> List[Dict[str, Any]]:
        """Return list of all orders from databse

        Returns:
            List[Dict[str, Any]]: List of order rows
        """


LOCAL_SYSTEM_DATABASE = []


class LocalSystem(AbstractSystem):
    def create_order(self, order_info: models.Order) -> models.SystemOrderResults:
        if order_info.company_name == 'Customer_a':
            return models.SystemOrderResults(status_code=501, error='Somesing is no yes')
        else:
            order_row = {
                "id": len(LOCAL_SYSTEM_DATABASE) + 1,
                "details": order_info.dict()
            }
            LOCAL_SYSTEM_DATABASE.append(order_row)
            return models.SystemOrderResults(status_code=201)

    @staticmethod
    def get_all_orders() -> List[Dict[str, Any]]:
        return LOCAL_SYSTEM_DATABASE


class RemoteSystem(AbstractSystem):
    @staticmethod
    def _connect2db():
        client = MongoClient('mongo', 27017,
                             username=os.environ["MONGO_USER"],
                             password=os.environ["MONGO_PASSWORD"])
        db = client['email2order']
        return db['orders']

    def create_order(self, order_info: models.Order) -> models.SystemOrderResults:
        orders = self._connect2db()
        orders.insert_one(order_info.dict())
        return models.SystemOrderResults(status_code=201)

    def get_all_orders(self) -> List[Dict[str, Any]]:
        orders = self._connect2db()
        order_list = orders.find({})
        return list(order_list)
