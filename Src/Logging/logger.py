from Src.Core.abstract_logic import abstract_logic
from Src.Core.event_type import event_type
from Src.Core.logger_level import logger_level
from Src.Managers.settings_manager import settings_manager
from Src.Services.observe_service import observe_service
from datetime import datetime


class logger(abstract_logic):
    
    
    def __init__(self, settings_manager: settings_manager):
        self.__file_path = "log.txt"
        self.manager = settings_manager
        observe_service.append(self)
        
        
    def log_error(self, details):
        self.__log(logger_level.ERROR.name, details)
    
    
    def log_info(self, details):
        self.__log(logger_level.INFO.name, details)
    
    
    def log_debug(self, details):
        self.__log(logger_level.DEBUG.name, details)
    
    
    def __log(self, level, message):
        timestamp = datetime.now().isoformat()
        log_output = f"[{timestamp}] {level}\t{message}"
        
        if not self.manager.settings.log_to_file:
            print(log_output)
        else:
            with open(self.__file_path, "a", encoding="utf-8") as file:
                file.write(f"{log_output}\n")
        
        
    def handle_event(self, type: event_type, params):
        super().handle_event(type, params)
        
        if type == event_type.ERROR and logger_level.ERROR.value >= self.manager.settings.min_log_level:
            self.log_error(params)
        if type == event_type.INFO and logger_level.INFO.value >= self.manager.settings.min_log_level:
            self.log_info(params)
        if type == event_type.DEBUG and logger_level.DEBUG.value >= self.manager.settings.min_log_level:
            self.log_debug(params)
    
    
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)