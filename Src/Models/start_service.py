from Src.Core.abstract_logic import abstract_logic
from .data_repository import data_repository
from Src.Core.validator import validator
from .group import group_model

class start_service(abstract_logic):
    __reposity:data_repository = None
    
    def __init__(self, reposity:data_repository) -> None:
        super().__init__()
        validator.validate(reposity, data_repository)
        self.__reposity = reposity
        
    def create_nomenclature_group(self):
        list = [group_model.default_group_cold(), group_model.default_group_source]
        self. __reposity.data[data_repository.group_key()] = list