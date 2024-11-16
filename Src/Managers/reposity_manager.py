from Src.Core.event_type import event_type
from Src.Core.validator import validator
from Src.Core.abstract_logic import abstract_logic
from Src.Managers.settings_manager import settings_manager
from Src.data_reposity import data_reposity
from Src.Services.observe_service import observe_service
from Src.DTO.domain_prototype import domain_prototype
from Src.DTO.filter import filter
from Src.Reports.report_factory import report_factory
import json


"""
Менеджер для репозитория
"""
class reposity_manager(abstract_logic):
   
    
    def __init__(self, reposity: data_reposity, settings_manager: settings_manager):
        observe_service.append(self)
        self.reposity = reposity
        self.manager = settings_manager
        self.file_name = "reposity_data.json"
        
        
    def save_reposity_data(self):
        report = report_factory(self.manager).create_default()
        reposity_data = {}
        for key, value in self.reposity.data.items():
            report.create(value)
            reposity_data[key] = json.loads(report.result)
            
        if reposity_data:
            try:
                with open(self.file_name, 'w', encoding='utf-8') as stream:
                    json.dump(reposity_data, stream, ensure_ascii=False, indent=4)
            except Exception as ex:
                raise Exception(f'Ошибка при сохранении данных! {ex}')
    
    
    def restore_reposity_data(self):
        return "Данные загружены!"
    
    
    def handle_event(self, type: event_type, params):
        super().handle_event(type, params)
        
        if type == event_type.SAVE_DATA_REPOSITY:
            return self.save_reposity_data()
        elif type == event_type.RESTORE_DATA_REPOSITY:
            return self.restore_reposity_data()
    