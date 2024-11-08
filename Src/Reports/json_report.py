from Src.Core.format_reporting import format_reporting
from Src.Core.abstract_report import abstract_report
from Src.Core.validator import validator, operation_exception
import json
from datetime import datetime
from enum import Enum

"""
Ответ формирует набор данных в формате JSON
"""
class json_report(abstract_report):

    def __init__(self) -> None:
       super().__init__()
       self.__format = format_reporting.JSON

 
    def create(self, data: list):
        validator.validate(data, list)
        if len(data) == 0:
            raise operation_exception("Набор данных пуст!")
        

        first_model = data[0]
        fields = self.get_class_fields(first_model)
        
        json_data = []
        
        # Данные
        for row in data:
            row_data = {}
            for field in fields:
                value = getattr(row, field)
                row_data[field] = self.__serialize(value)
            json_data.append(row_data)
        
        self.result = json.dumps(json_data, indent=4, ensure_ascii=False)
    
    def __serialize(self, value):
        if isinstance(value, list):
            return [self.__serialize(item) for item in value]
        elif hasattr(value, "to_dict"):
            return value.to_dict()
        elif hasattr(value, "__dict__"):
            return {key: self.__serialize(val) for key, val in value.__dict__.items() if not key.startswith("_")}
        elif isinstance(value, dict):
             return {key: self.__serialize(val) for key, val in value.items() if not key.startswith("_")}
        elif isinstance(value, datetime):
            return datetime.timestamp(value)
        elif isinstance(value, Enum):
            return value.value
        else:
            return value