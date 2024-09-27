from Src.Core.abstract_logic import abstract_logic
from Src.Core.abstract_report import abstract_report
from Src.Core.format_reporting import format_reporting
from Src.Reports.csv_report import csv_report
from Src.Core.validator import validator, operation_exception


"""
Фабрика для формирования отчетов
"""
class report_factory(abstract_logic):
    __reports = {}

    def __init__(self) -> None:
        super().__init__()
        # Наборы отчетов
        self.__reports[ format_reporting.CSV ] = csv_report


    """
    Получить инстанс нужного отчета
    """
    def create(self, format: format_reporting) ->  abstract_report: 
        validator.validate(format, format_reporting)
        
        if format not in self.__reports.keys() :
            self.set_exception( operation_exception(f"Указанный вариант формата {format} не реализован!"))
            return None
        
        report = self.__reports[format]
        return report()
    

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)