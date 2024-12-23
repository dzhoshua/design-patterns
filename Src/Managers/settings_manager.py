from Src.Core.event_type import event_type
from Src.settings import settings
from Src.Core.abstract_logic import abstract_logic
from Src.Core.abstract_report import abstract_report
from Src.Core.validator import validator, operation_exception, argument_exception
from Src.Core.format_reporting import format_reporting
from Src.Core.logger_level import logger_level
import json
import os
from datetime import datetime


"""
Менеджер настроек
"""
class settings_manager(abstract_logic):
    __file_name = "settings.json"
    __settings: settings = None
    __report_settings = {
        "CSV": "csv_report",
        "MARKDOWN": "markdown_report",
        "JSON": "json_report",
        "XML": "xml_report",
        "RTF": "rtf_report"
    }


    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance 
     

    def __init__(self) -> None:
        if self.__settings is None:
            self.__settings = self.__default_setting()
    

    """
    Загруженные настройки
    """
    @property
    def settings(self) -> settings:
        return self.__settings
    
    @property
    def report_settings(self):
        return self.__report_settings
        

    """
    Открыть и загрузить настройки
    """
    def open(self, file_name:str = ""):
        if file_name != "":
            validator.validate(file_name, str)
            self.__file_name = file_name

        try:
            full_name = self.file_search(self.__file_name)
            stream = open(full_name, encoding='utf-8')
            data = json.load(stream)

            # Список полей от типа назначения    
            fields = list(filter(lambda x: not x.startswith("_"), dir(self.__settings.__class__)))

            # Заполняем свойства 
            for field in fields:
                keys = list(filter(lambda x: x == field, data.keys()))
                if len(keys) != 0:
                    value = data[field]

                    # Если обычное свойство - заполняем.
                    if not isinstance(value, list) and not isinstance(value, dict):
                        setattr(self.__settings, field, value)
            return True
        except Exception as ex :
            self.__settings = self.__default_setting()
            self.set_exception(ex)
            return False
        
    
    def save(self):
        file_path = os.path.join(os.curdir, self.__file_name)

        settings_data = {
            "organization_name": self.__settings.organization_name,
            "inn": self.__settings.inn,
            "account": self.__settings.account,
            "correspondent_account": self.__settings.correspondent_account,
            "biс": self.__settings.bic,
            "organization_type": self.__settings.organization_type,
            "block_period": self.__settings.block_period,
            "first_start" : self.__settings.first_start,
            "min_log_level" : self.__settings.min_log_level,
            "save_to_file": self.__settings.save_to_file
        }

        try:
            with open(file_path, 'w', encoding='utf-8') as stream:
                json.dump(settings_data, stream, ensure_ascii=False, indent=4)
        except Exception as ex:
            self.set_exception(ex)
            raise
    
    
    """
    Набор настроек по умолчанию
    """
    def __default_setting(self) -> settings:
        _settings = settings()
        _settings.inn = "380080920202"
        _settings.organization_name = "Рога и копыта (default)"
        _settings.account = "98745632107"
        _settings.correspondent_account = "12345678901"
        _settings.bic = "123456789"
        _settings.organization_type = "12345"
        _settings.block_period = "2024-01-01"
        _settings.first_start = True
        _settings.save_to_file = True
        _settings.min_log_level = logger_level.INFO.value
        
        return _settings
    
    
    def get_report_class(self, format: format_reporting = None) -> abstract_report:
        if format is None:
            format = self.__settings.report_format

        validator.validate(format, format_reporting)
        report_class = self.report_settings.get(format.name, None)

        return report_class()
          
    
    def handle_event(self, type: event_type, params):
        return super().handle_event(type, params)
    
    
    """
    Перегрузка абстрактного метода
    """
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)