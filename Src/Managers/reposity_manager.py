from Src.Core.event_type import event_type
from Src.Core.validator import validator
from Src.Core.abstract_logic import abstract_logic
from Src.Managers.settings_manager import settings_manager
from Src.data_reposity import data_reposity


"""
Менеджер для репозитория
"""
class reposity_manager(abstract_logic):
    __file_name: str = "reposity_data.json"
    __settings_manager: settings_manager = None
    __reposity: data_reposity = None
    
    
    def handle_event(self, type: event_type, params):
        return super().handle_event(type, params)