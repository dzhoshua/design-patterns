from abc import ABC, abstractmethod
from Src.Core.validator import validator
from Src.Models.warehouse_transaction import warehouse_transaction


class abstract_processing:
    @abstractmethod
    def processing(self, transactions: list[warehouse_transaction]):
        pass