from Src.Core.base_models import base_model_code
from Src.Core.validator import argument_exception, validator


class balanse_sheet(base_model_code):
    __income: list = None
    __expenditure: list = None
    __opening_remainder: list = None
    __remainder: list = None
    
    
    """
    Приход
    """
    @property
    def income(self) -> list:
        return self.__income
    
    @income.setter
    def income(self, value: list):
        validator.validate(value, list)
        self.__income = value


    """
    Расход
    """
    @property
    def expenditure(self) -> list:
        return self.__expenditure
    
    @expenditure.setter
    def expenditure(self, value: list):
        validator.validate(value, list)
        self.__expenditure = value
        
        
    """
    Начальные остатки
    """
    @property
    def opening_remainder(self) -> list:
        return self.__opening_remainder
    
    @opening_remainder.setter
    def opening_remainder(self, value: list):
        validator.validate(value, list)
        self.__opening_remainder = value
        
        
    """
    Обороты
    """
    @property
    def remainder(self) -> list:
        return self.__remainder
    
    @remainder.setter
    def remainder(self, value: list):
        validator.validate(value, list)
        self.__remainder = value

   
    def to_dict(self):
        return {
            "unique_code": self.unique_code,
            "opening_remainder": self.opening_remainder,
            "income": self.income,
            "expenditure": self.expenditure,
            "remainder": self.remainder,
        }
        
        
    """
    Фабричный метод
    """
    @staticmethod
    def create(income: list, expenditure: list, opening_remainder: list, remainder:list):

        item = balanse_sheet()
        item.income = income
        item.expenditure = expenditure
        item.opening_remainder = opening_remainder
        item.remainder = remainder
        return item