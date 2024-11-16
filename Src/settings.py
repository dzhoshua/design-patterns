from Src.Core.validator import validator
from Src.Reports.report_factory import format_reporting
from datetime import datetime

"""
Настройки
"""
class settings:
    __organization_name: str = ""
    __inn: str = ""
    __account: str = ""
    __correspondent_account: str = ""
    __bic: str = ""
    __organization_type: str = ""
    __report_format: format_reporting = format_reporting.JSON
    __block_period: str = ""
    __first_start: bool = True

    """
    Наименование организации
    """
    @property
    def organization_name(self):
        return self.__organization_name
    

    @organization_name.setter
    def organization_name(self, value:str):
        validator.validate(value, str, 255)
        self.__organization_name = value

    """
    ИНН
    """
    @property
    def inn(self):
        return self.__inn

    @inn.setter
    def inn(self, value:str):
        validator.validate(value, str, 12)
        self.__inn = value
        
    
    """
    Счет
    """
    @property
    def account(self):
        return self.__account

    @account.setter
    def account(self, value:str):
        validator.validate(value, str, 11)
        self.__account = value
        
    """
    Корреспондентский счет
    """
    @property
    def correspondent_account(self):
        return self.__correspondent_account

    @correspondent_account.setter
    def correspondent_account(self, value:str):
        validator.validate(value, str, 11)
        self.__correspondent_account = value
        
    
    """
    БИК
    """
    @property
    def bic(self):
        return self.__bic

    @bic.setter
    def bic(self, value:str):
        validator.validate(value, str, 9)
        self.__bic = value
        
        
    """
    Вид собственности
    """
    @property
    def organization_type(self):
        return self.__organization_type

    @organization_type.setter
    def organization_type(self, value:str):
        validator.validate(value, str, 5)
        self.__organization_type = value
    
    """
    Вид отчета
    """
    @property
    def report_format(self):
        return self.__report_format

    @report_format.setter
    def report_format(self, value:str):
        validator.validate(value, format_reporting)
        self.__report_format = value
        
        
    @property
    def block_period(self):
        return self.__block_period
    
    @block_period.setter
    def block_period(self, value: str):
        validator.validate(value, str)
        self.__block_period = value
        
        
    @property
    def first_start(self):
        return self.__first_start
    
    @first_start.setter
    def first_start(self, value: bool):
        validator.validate(value, bool)
        self.__first_start = value
