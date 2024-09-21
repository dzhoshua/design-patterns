from Src.Core.abstract_logic import abstract_logic
from Src.data_reposity import data_reposity
from Src.Core.validator import validator
from Src.Models.group import group_model
from Src.settings_manager import settings_manager
from Src.settings import settings

"""
Сервис для реализации первого старта приложения
"""
class start_service(abstract_logic):
    __reposity: data_reposity = None
    __settings_manager: settings_manager = None

    def __init__(self, reposity: data_reposity, manager: settings_manager ) -> None:
        super().__init__()
        validator.validate(reposity, data_reposity)
        validator.validate(manager, settings_manager)
        self.__reposity = reposity
        self.__settings_manager = manager

    """
    Текущие настройки
    """
    @property 
    def settings(self) -> settings:
        return self.__settings_manager.settings

    """
    Сформировать группы номенклатуры
    """
    def __create_nomenclature_groups(self):
        list = []
        list.append(group_model.default_group_cold())
        list.append( group_model.default_group_source())
        self.__reposity.data[data_reposity.group_key()] = list    

    """
    Первый старт
    """
    def create(self):
        self.__create_nomenclature_groups()


    """
    Перегрузка абстрактного метода
    """
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)    


