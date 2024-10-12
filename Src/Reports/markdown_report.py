from Src.Core.format_reporting import format_reporting
from Src.Core.abstract_report import abstract_report
from Src.Core.validator import validator, operation_exception


"""
Ответ формирует набор данных в формате CSV
"""
class markdown_report(abstract_report):

    def __init__(self) -> None:
       super().__init__()
       self.__format = format_reporting.MARKDOWN

 
    def create(self, data: list):
        validator.validate(data, list)
        if len(data) == 0:
            raise operation_exception("Набор данных пуст!")
        
        
        first_model = data[0]
        fields = self.get_class_fields(first_model)
        
        # Заголовок
        self.result += "| " + " | ".join(fields) + " |\n"
        
        # Разделитель
        self.result += "| " + " | ".join(["---"] * len(fields)) + " |\n"
        
        # Данные
        for row in data:
            row_data = [str(getattr(row, field)) for field in fields]
            self.result += "| " + " | ".join(row_data) + " |\n"