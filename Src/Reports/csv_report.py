from Src.Core.format_reporting import format_reporting
from Src.Core.abstract_report import abstract_report
from Src.Core.validator import validator, operation_exception


"""
Ответ формирует набор данных в формате CSV
"""
class csv_report(abstract_report):

    def __init__(self) -> None:
       super().__init__()
       self.__format = format_reporting.CSV

 
    def create(self, data: list):
        validator.validate(data, list)
        if len(data) == 0:
            raise operation_exception("Набор данных пуст!")
        

        first_model = data[0]

        # Список полей от типа назначения    
        fields = self.get_class_fields(first_model)
        # Заголовок
        for field in fields:
            self.result += f"{str(field)};"

        self.result += "\n"    

        # Данные
        for row in data:
            for field in fields:
            
                value = getattr(row, field)
                self.result += f"{str(value)};"
            self.result += "\n"