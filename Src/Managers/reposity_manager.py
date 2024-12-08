from Src.Core.event_type import event_type
from Src.Core.abstract_logic import abstract_logic
from Src.Managers.settings_manager import settings_manager
from Src.data_reposity import data_reposity
from Src.Services.observe_service import observe_service
from Src.Reports.report_factory import report_factory
from Src.Reports.json_deserializer import json_deserializer
from Src.Services.database_service import database_service
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
        if self.manager.settings.data_to_db:
            self.db_service = database_service()
            self.db_service.init_database()
            
        observe_service.append(self)
        
        
    """
    Сохранение данных из репозитория
    """
    def save_reposity_data(self):
        report = report_factory(self.manager).create_default()
        
        if self.manager.settings.data_to_db:
            message = self.__to_database(report)
        else:
            message = self.__to_file(report)
        
        return message
     
    
    # Запись в файл      
    def __to_file(self, report):
        reposity_data = {}
        
        for key, value in self.reposity.data.items():
            report.create(value)
            reposity_data[key] = json.loads(report.result)
            
        if reposity_data:
            try:
                data = json.dumps(reposity_data, indent=4, ensure_ascii=False)
                with open(self.file_name , 'w', encoding='utf-8') as f:
                    f.write(data)
                    
                message = "Данные сохранены в файл."
                observe_service.raise_event(event_type.INFO, message)
                return message
            except Exception as ex:
                message = f"Ошибка при сохранении данных в файл! {ex}"
                observe_service.raise_event(event_type.ERROR, message)
                return message
    
    
    # Запись в базу данных
    def __to_database(self, report):
        for key, value in self.reposity.data.items():
            
            observe_service.raise_event(event_type.INFO, f"Сохранение данных в таблицу {key}...")
            
            for item in value:
                id = item.unique_code
                name = item.name or None
                report.create(item)
                document = report.result
                
                observe_service.raise_event(event_type.DEBUG, f'Сохранение {name}')
                observe_service.raise_event(event_type.DEBUG, f'{document}')
                
                try:
                    self.db_service.write(key, id, name, document)
                except Exception as ex:
                    return ex
                
                return "Данные успешно загружены в базу данных."
            
    
    """
    Загрузка данных в репозиторий
    """
    def restore_reposity_data(self):
        if self.manager.settings.data_to_db:
            message = self.__from_database()
        else:
            message = self.__from_file()
        
        return message
    
    
    def __from_file(self):
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
        message = "Данные успешно загружены из файла."
        observe_service.raise_event(event_type.INFO, message)
        return message
    
    
    def __from_database(self):
        for key, model in data_reposity.keys_and_models():
            data = self.db_service.read(key)
            for row in data:
                # достаём данные из document поля
                pass
                
        message = "Данные успешно загружены из базы данных."
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
    