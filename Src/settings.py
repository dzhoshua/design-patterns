from Src.Core.validator import validator
from Src.Reports.report_factory import format_reporting
from Src.Core.event_type import event_type
from Src.Core.logger_level import logger_level
from Src.Services.observe_service import observe_service
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
    __min_log_level:int = None
    __save_to_file: bool = True


    """
    Наименование организации
    """
    @property
    def organization_name(self):
        return self.__organization_name
    

    @organization_name.setter
    def organization_name(self, value:str):
        try:
            validator.validate(value, str, 255)
        except Exception as ex:
            observe_service.raise_event(event_type.ERROR, f"organization_name: {ex}")
        self.__organization_name = value
        observe_service.raise_event(event_type.DEBUG, f"Наименование организации (organization_name): {value}")


    """
    ИНН
    """
    @property
    def inn(self):
        return self.__inn

    @inn.setter
    def inn(self, value:str):
        try:
            validator.validate(value, str, 12)
        except Exception as ex:
            observe_service.raise_event(event_type.ERROR, f"inn: {ex}")
        self.__inn = value
        observe_service.raise_event(event_type.DEBUG, f"ИНН (inn): {value}")
        
    
    """
    Счет
    """
    @property
    def account(self):
        return self.__account

    @account.setter
    def account(self, value:str):
        try:
            validator.validate(value, str, 11)
        except Exception as ex:
            observe_service.raise_event(event_type.ERROR, f"account: {ex}")
        self.__account = value
        observe_service.raise_event(event_type.DEBUG, f"Счет (account): {value}")
        
    """
    Корреспондентский счет
    """
    @property
    def correspondent_account(self):
        return self.__correspondent_account

    @correspondent_account.setter
    def correspondent_account(self, value:str):
        try:    
            validator.validate(value, str, 11)
        except Exception as ex:
            observe_service.raise_event(event_type.ERROR, f"correspondent_account: {ex}")
        self.__correspondent_account = value
        observe_service.raise_event(event_type.DEBUG, f"Корреспондентский счет (correspondent_account): {value}")
        
    
    """
    БИК
    """
    @property
    def bic(self):
        return self.__bic

    @bic.setter
    def bic(self, value:str):
        try:
            validator.validate(value, str, 9)
        except Exception as ex:
            observe_service.raise_event(event_type.ERROR, f"bic: {ex}")
        self.__bic = value
        observe_service.raise_event(event_type.DEBUG, f"БИК (bic): {value}")
        
        
    """
    Вид собственности
    """
    @property
    def organization_type(self):
        return self.__organization_type

    @organization_type.setter
    def organization_type(self, value:str):
        try:
            validator.validate(value, str, 5)
        except Exception as ex:
            observe_service.raise_event(event_type.ERROR, f"organization_type: {ex}")
        self.__organization_type = value
        observe_service.raise_event(event_type.DEBUG, f"Вид собственности (organization_type): {value}")
    
    """
    Вид отчета
    """
    @property
    def report_format(self):
        return self.__report_format

    @report_format.setter
    def report_format(self, value:format_reporting):
        try:
            validator.validate(value, format_reporting)
        except Exception as ex:
            observe_service.raise_event(event_type.ERROR, f"report_format: {ex}")
        self.__report_format = value
        observe_service.raise_event(event_type.DEBUG, f"Вид отчета (report_format): {value}")
       
        
    """
    Дата блокировки
    """ 
    @property
    def block_period(self):
        return self.__block_period
    
    @block_period.setter
    def block_period(self, value: str):
        try:
            validator.validate(value, str)
        except Exception as ex:
            observe_service.raise_event(event_type.ERROR, f"block_period: {ex}")
        self.__block_period = value
        observe_service.raise_event(event_type.DEBUG, f"Дата блокировки (block_period): {value}")
        
    
    """
    Первый старт
    """    
    @property
    def first_start(self):
        return self.__first_start
    
    @first_start.setter
    def first_start(self, value: bool):
        try:
            validator.validate(value, bool)
        except Exception as ex:
            observe_service.raise_event(event_type.ERROR, f"first_start: {ex}")
        self.__first_start = value
        observe_service.raise_event(event_type.DEBUG, f"Первый старт (first_start): {value}")
        
        
    """
    Минимальный уровень логирования
    """
    @property
    def min_log_level(self):
        return self.__min_log_level

    @min_log_level.setter
    def min_log_level(self, value: int):
        try:
            validator.validate(value, int)
        except Exception as ex:
            observe_service.raise_event(event_type.ERROR, f"first_start: {ex}")
        self.__min_log_level = value
        observe_service.raise_event(event_type.DEBUG, f"Минимальный уровень логирования (min_log_level): {value}")
        
        
    """
    Сохранение логов в файл
    """    
    @property
    def save_to_file(self):
        return self.__save_to_file
    
    @save_to_file.setter
    def save_to_file(self, value: bool):
        try:
            validator.validate(value, bool)
        except Exception as ex:
            observe_service.raise_event(event_type.ERROR, f"save_to_file: {ex}")
        self.__save_to_file = value
        observe_service.raise_event(event_type.DEBUG, f"Сохранение логов в файл (save_to_file): {value}")
