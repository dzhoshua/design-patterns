from Src.Core.abstract_filter import abstract_filter
from Src.DTO.filter import filter
from Src.Core.validator import validator
from Src.Core.format_filter import format_filter
from Src.Models.nomenclature import nomenclature_model
from Src.Models.range import range_model


class domain_prototype(abstract_filter):

    def __init__(self, source: list) -> None:
        super().__init__(source)


    def create(self, data: list, filterDTO: filter):
        validator.validate(data, list)
        validator.validate(filterDTO, filter)

        self.data = self.get_filtered_name(filterDTO)
        self.data = self.get_filtered_id(filterDTO)
        domains = domain_prototype(self.data)
        return domains
    
    
    def get_filtered_name(self, filterDTO: filter) -> list:
        if filterDTO.name is None or filterDTO.name == "":
            return self.data
        
        result = []
        for item in self.data:
            if isinstance(item, range_model) and item.base is not None:
                item_names = [item.name, item.base.name]
            elif isinstance(item, nomenclature_model):
                item_names = [item.name]
            else:
                item_names = [item.name]

            for item_name in item_names:
                if filterDTO.filter_name == format_filter.EQUALS:
                    if item_name == filterDTO.name:
                        result.append(item)
                        
                elif filterDTO.filter_name == format_filter.LIKE:
                    if filterDTO.name in item_name:
                        result.append(item)

        return result
        
    
    def get_filtered_id(self, filterDTO: filter) -> list:
        if filterDTO.unique_code is None or filterDTO.unique_code == "":
            return self.data
        
        result = []
        for item in self.data:
            if filterDTO.filter_unique_code == format_filter.EQUALS:
                if str(item.unique_code) == filterDTO.unique_code:
                    result.append(item)
            elif filterDTO.filter_unique_code == format_filter.LIKE:
                if filterDTO.unique_code in str(item.unique_code):
                    result.append(item)

        return result