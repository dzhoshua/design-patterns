from Src.start_service import start_service
from Src.data_reposity import data_reposity
from Src.Reports.csv_report import csv_report
from Src.Reports.report_factory import report_factory
from Src.Core.format_reporting import format_reporting
from Src.Reports.csv_report import csv_report

import unittest


"""
Набор тестов для проверки работы формирование отчетов
"""
class test_reporting(unittest.TestCase):
    
    """
    Проверка работы отчеиа CSV
    """
    def test_csv_report_create_range(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()
        report = csv_report()

        # Действие
        report.create(reposity.data[ data_reposity.range_key()  ])

        # Проверки
        assert report.result != ""


    """
    Проверка работы отчеиа CSV
    """
    def test_csv_report_create_nomenclature(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()
        report = csv_report()

        # Действие
        report.create(reposity.data[ data_reposity.nomenclature_key()  ])

        # Проверки
        assert report.result != ""    

    """
    Проверить работу фабрики для получения инстанса нужного отчета
    """
    def test_report_factory_create(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()        
       
        # Действие
        report = report_factory().create( format_reporting.CSV )

        # Проверка
        assert report is not None
        assert isinstance(report,  csv_report)

    """
    Проверить работу фабрики. Не реализован формат
    """
    def test_report_factory_create_fail(self):
         # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()        
        factory = report_factory()
       
        # Действие
        report = factory.create( format_reporting.MARKDOWN )

        # Проверка
        assert report is None
        assert factory.is_error == True