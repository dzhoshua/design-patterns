from Src.Core.abstract_logic import abstract_logic
from Src.Core.event_type import event_type
from Src.Core.validator import validator
from Src.Core.logger_level import logger_level
from Src.Managers.settings_manager import settings_manager
from Src.Services.observe_service import observe_service
from datetime import datetime


class logger(abstract_logic):
    
    
    def __init__(self, settings_manager: settings_manager):
        self.manager = settings_manager
        observe_service.append(self)
        
        
    def log_error(self, details):
        pass
    
    
    def log_info(self, details):
        pass
    
    
    def log_debug(self, details):
        pass
        
        
    def handle_event(self, type: event_type, params):
        super().handle_event(type, params)
        
        if type == logger_level.ERROR and self.manager.settings.min_log_level >= logger_level.ERROR.value:
            self.log_error(params)
        if type == logger_level.INFO and self.manager.settings.min_log_level >= logger_level.INFO.value:
            self.log_info(params)
        if type == logger_level.DEBUG and self.manager.settings.min_log_level >= logger_level.DEBUG.value:
            self.log_debug(params)
    
    
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)