from Src.Core.event_type import event_type
from Src.Core.validator import validator
from Src.Core.abstract_logic import abstract_logic
from Src.Managers.settings_manager import settings_manager
from Src.data_reposity import data_reposity
from datetime import datetime


"""
Формирование ОСВ
"""
class turnover_balanse_sheet(abstract_logic):
    __date_start: datetime
    __date_end: datetime
    __warehouse_name: str = ""
    
    
    @property
    def date_start(self) -> datetime:
        return self.__date_start
    
    @date_start.setter
    def date_start(self, value: datetime):
        validator.validate(value, datetime)
        self.__date_start = value
        
    
    @property
    def date_end(self) -> datetime:
        return self.__date_end
    
    @date_end.setter
    def date_end(self, value: datetime):
        validator.validate(value, datetime)
        self.__date_end = value
    
    
    @property
    def warehouse_name(self) -> str:
        return self.__warehouse_name
    
    @warehouse_name.setter
    def warehouse_name(self, value: str):
        validator.validate(value, str, 255)
        self.__warehouse_name = value.strip()
     
    
    def handle_event(self, type: event_type, params):
        return super().handle_event(type, params)