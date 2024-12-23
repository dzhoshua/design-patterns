from Src.Core.event_type import event_type
from Src.Core.abstract_logic import abstract_logic
from Src.Managers.settings_manager import settings_manager
from Src.data_reposity import data_reposity
from Src.Services.observe_service import observe_service
from Src.Reports.report_factory import report_factory
from Src.Reports.json_deserializer import json_deserializer
from Src.Core.logger_level import logger_level
import json
import os


"""
Менеджер для репозитория
"""
class reposity_manager(abstract_logic):
   
    
    def __init__(self, reposity: data_reposity, settings_manager: settings_manager):
        self.reposity = reposity
        self.manager = settings_manager
        self.file_name = "reposity_data.json"
        observe_service.append(self)
        
        
    """
    Сохранение данных из репозитория в файл
    """
    def save_reposity_data(self):
        report = report_factory(self.manager).create_default()
        reposity_data = {}
        for key, value in self.reposity.data.items():
            report.create(value)
            reposity_data[key] = json.loads(report.result)
        if reposity_data:
            try:
                data = json.dumps(reposity_data, indent=4, ensure_ascii=False)
                with open(self.file_name , 'w', encoding='utf-8') as f:
                    f.write(data)
                    
                message = "Данные сохранены в файл!"
                observe_service.raise_event(event_type.INFO, message)
                return message
            except Exception as ex:
                message = f"Ошибка при сохранении данных! {ex}"
                observe_service.raise_event(event_type.ERROR, message)
                return message
            
    
    """
    Загрузка данных из файла в репозиторий
    """
    def restore_reposity_data(self):
        if not os.path.exists(self.file_name):
            message = "Файл не найден. Сохраните данные."
            observe_service.raise_event(event_type.ERROR, message)
            return message
        try:
            with open(self.file_name , 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as ex:
            observe_service.raise_event(event_type.ERROR, ex)
            return ex
            
        models = data_reposity.keys_and_models()
        for key, list in data.items():
            if key in models.keys():
                deserializer = json_deserializer(models[key])
                deserializer.open(self.file_name, data_list=list)
                
                self.reposity.data[key] = deserializer.model_objects
        message = "Данные загружены!"
        observe_service.raise_event(event_type.INFO, message)
        return message
    
    
    def handle_event(self, type: event_type, params):
        super().handle_event(type, params)
        if type == event_type.SAVE_DATA_REPOSITY:
            return self.save_reposity_data()
        elif type == event_type.RESTORE_DATA_REPOSITY:
            return self.restore_reposity_data()
        
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)
    