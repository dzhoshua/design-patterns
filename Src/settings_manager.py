from Src.settings import settings
from Src.Core.abstract_logic import abstract_logic
from Src.Core.abstract_report import abstract_report
from Src.Core.validator import validator, operation_exception, argument_exception
from Src.Core.format_reporting import format_reporting


import json
import os
from datetime import datetime

"""
Менеджер настроек
"""
class settings_manager(abstract_logic):
    __file_name = "settings.json"
    __settings:settings = None
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
    Открыть и загрузить настройки
    """
    def open(self, file_name:str = ""):
        validator.validate(file_name, str)
        
        if file_name != "":
            self.__file_name = file_name

        try:
            current_path_info = os.path.split(__file__)
            current_path = current_path_info[0]
            full_name = f"{current_path}{os.sep}{self.__file_name}"
            stream = open(full_name)
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
        _settings.block_period =  "2024-01-01"
        return _settings
    
    
    def get_report_class(self, format: format_reporting = None) -> abstract_report:
        if format is None:
            format = self.__settings.report_format

        validator.validate(format, format_reporting)
        report_class = self.report_settings.get(format.name, None)

        return report_class()
    
    
    def save(self):
        file_path = os.path.join(os.curdir, self.__file_name)

        settings_data = {
            "organization_name": self.__settings.organization_name,
            "inn": self.__settings.inn,
            "account": self.__settings.account,
            "correspondent_account": self.__settings.correspondent_account,
            "biс": self.__settings.bik,
            "organization_type": self.__settings.organization_type,
            "block_period": self.__settings.block_period
        }

        try:
            with open(file_path, 'w', encoding='utf-8') as stream:
                json.dump(settings_data, stream, ensure_ascii=False, indent=4)
        except Exception as ex:
            self.set_exception(ex)
            raise
    
    
    """
    Перегрузка абстрактного метода
    """
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)