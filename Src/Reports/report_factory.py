from Src.Core.abstract_logic import abstract_logic
from Src.Core.abstract_report import abstract_report
from Src.Core.format_reporting import format_reporting
from Src.Reports.csv_report import csv_report
from Src.Reports.json_report import json_report
from Src.Reports.xml_report import xml_report
from Src.Reports.markdown_report import markdown_report
from Src.Reports.rtf_report import rtf_report
from Src.Core.validator import validator, operation_exception
from Src.settings_manager import settings_manager
from Src.settings import settings


"""
Фабрика для формирования отчетов
"""
class report_factory(abstract_logic):
    __reports:dict = {}
    __settings_manager: settings_manager = None
    __reports_setting: dict = {}

    def __init__(self, manager: settings_manager) -> None:
        super().__init__()
        # Наборы отчетов
        self.__reports[format_reporting.CSV] = csv_report
        self.__reports[format_reporting.MARKDOWN] = markdown_report
        self.__reports[format_reporting.JSON] = json_report
        self.__reports[format_reporting.RTF] = rtf_report
        self.__reports[format_reporting.XML] = xml_report
        
        self.__settings_manager = manager


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
    
    @property
    def reports_setting(self) -> dict:
        return self.__reports_setting
    
    @reports_setting.setter
    def reports_setting(self, reports_setting: dict):
        validator.validate(reports_setting, dict)
        self.__reports_setting = reports_setting



    @property
    def reports(self) -> dict:
        return self.__reports
    @reports.setter
    def reports(self, reports: dict):
        validator.validate(reports, dict)
        self.__reports = reports
        
    """
    Текущие настройки
    """
    @property 
    def settings(self) -> settings:
        return self.__settings_manager.settings
    
    def load_formats_from_settings(self) -> None:
        tmp_reports_setting = {}
        for key, value in self.__settings_manager.report_settings.items():
            try:
                tmp_reports_setting[format_reporting[key]] = value
            except Exception as ex:
                self.set_exception(ex)
        self.reports_setting = tmp_reports_setting
    

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)
    