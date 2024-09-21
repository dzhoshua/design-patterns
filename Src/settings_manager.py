from Src.settings import settings
from Src.Core.abstract_logic import abstract_logic
from Src.Core.validator import validator


import json
import os

"""
Менеджер настроек
"""
class settings_manager(abstract_logic):
    __file_name = "settings.json"
    __settings:settings = None


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
        return _settings
    

    """
    Перегрузка абстрактного метода
    """
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)