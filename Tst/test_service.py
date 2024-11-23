import unittest
from Src.data_reposity import data_reposity
from Src.Managers.settings_manager import settings_manager
from Src.Core.event_type import event_type
from Src.Services.start_service import start_service
from Src.Services.nomenclature_service import nomenclature_service
from Src.Services.observe_service import observe_service
from Src.DTO.filter import filter
from Src.DTO.domain_prototype import domain_prototype

"""
Набор тестов для сервиса номенклатуры
"""
class test_nomenclature_service(unittest.TestCase):
    reposity = data_reposity()
    manager = settings_manager()
    start = start_service(reposity, manager)
    _nomenclature_service = nomenclature_service(reposity)
    start.create()
    
    def test_get_nomenclature(self):
        # Подготовка
        data = self.reposity.data[data_reposity.nomenclature_key()]
        unique_code = data[0].unique_code

        # Действие
        nom_data = self._nomenclature_service.get_nomenclature(data, unique_code)

        # Проверка
        assert len(nom_data) == 1
        assert nom_data[0] == data[0]
    
    
    def test_put_nomenclature(self):
        # Подготовка
        len_nom = len(self.reposity.data[data_reposity.nomenclature_key()])
        
        name = "Рис"
        range_id = self.reposity.data[data_reposity.range_key()][0].unique_code
        group_id = self.reposity.data[data_reposity.group_key()][0].unique_code

        # Действие
        self._nomenclature_service.put_nomenclature(name, group_id, range_id)

        # Проверка
        assert len(self.reposity.data[data_reposity.nomenclature_key()]) - len_nom == 1
        assert self.reposity.data[data_reposity.nomenclature_key()][-1].name == "Рис"
    
    
    def test_patch_nomenclature(self):
        # Подготовка
        old_nom = self.reposity.data[data_reposity.nomenclature_key()][0]
        data = {
            "unique_code":self.reposity.data[data_reposity.nomenclature_key()][0].unique_code,
            "name": "Подсолнечное масло",
            "group_id": self.reposity.data[data_reposity.group_key()][0].unique_code,
            "range_id": self.reposity.data[data_reposity.range_key()][0].unique_code
        }

        # Действие
        observe_service.raise_event(event_type.CHANGE_NOMENCLATURE, data)
        
        updated_nom = self.reposity.data[data_reposity.nomenclature_key()][0]

        # Проверка
        assert old_nom.unique_code == updated_nom.unique_code
        assert updated_nom.name == "Подсолнечное масло"
    
    
    def test_delete_nomenclature(self):
        # Подготовка
        data = self.reposity.data[data_reposity.nomenclature_key()]
        unique_code = data[0].unique_code

        # Действие
        observe_service.raise_event(event_type.DELETE_NOMENCLATURE, unique_code)
        
        data = self.reposity.data[data_reposity.nomenclature_key()]
        item_filter = filter.create({"unique_code": unique_code})
        prototype = domain_prototype(data)
        prototype.create(item_filter)
        
        # Проверка
        assert len(prototype.data) != 0