from Src.start_service import start_service
from Src.data_reposity import data_reposity
from Src.Reports.csv_report import csv_report
from Src.Reports.xml_report import xml_report
from Src.Reports.json_report import json_report
from Src.Reports.rtf_report import rtf_report
from Src.Reports.markdown_report import markdown_report
from Src.Reports.report_factory import report_factory
from Src.Core.format_reporting import format_reporting
from Src.settings_manager import settings_manager

import unittest
import os


"""
Набор тестов для проверки работы формирование отчетов
"""
class test_reporting(unittest.TestCase):
    __reports_path = "./Tst/reports_res"

    def __check_folder_exists(self) -> None:
        if not (os.path.exists(self.__reports_path) and os.path.isdir(self.__reports_path)):
            os.makedirs(self.__reports_path)
    
    def __save_file(self, file_name: str, result) -> None:
        with open(os.path.join(self.__reports_path, file_name), 'w', encoding='utf-8') as f:
            f.write(result)
            
    """
    Проверить работу фабрики для получения инстанса нужного отчета
    """
    def test_report_factory_create(self):
        # Подготовка
        set_manager = settings_manager()

        # Действие
        report = report_factory(set_manager).create(format_reporting.CSV)

        # Проверка
        assert report is not None
        assert isinstance(report, csv_report)
    
    """
    Проверка работы отчета CSV
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
        
        self.__check_folder_exists()
        file_name = f"{data_reposity.range_key()}.csv"
        self.__save_file(file_name, report.result)


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
        
        self.__check_folder_exists()
        file_name = f"{data_reposity.nomenclature_key()}.csv"
        self.__save_file(file_name, report.result)  
        
    def test_csv_report_create_group(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()

        report = csv_report()

        # Действие
        report.create(reposity.data[data_reposity.group_key()])

        # Проверка
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.group_key()}.csv"
        self.__save_file(file_name, report.result) 
        
    def test_csv_report_create_receipt(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()

        report = csv_report()

        # Действие
        report.create(reposity.data[data_reposity.receipt_key()])

        # Проверка
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.receipt_key()}.csv"
        self.__save_file(file_name, report.result)
        
        
    """
    MARKDOWN
    """
    def test_md_report_create_range(self):
        # Подготовка
        
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()

        report = markdown_report()

        # Действие
        report.create(reposity.data[data_reposity.range_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.range_key()}.md"
        self.__save_file(file_name, report.result)

   
    def test_md_report_create_nomenclature(self):
        # Подготовка
        
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()

        report = markdown_report()

        # Действие
        report.create(reposity.data[data_reposity.nomenclature_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.nomenclature_key()}.md"
        self.__save_file(file_name, report.result)

    
    
    def test_md_report_create_group(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()

        report = markdown_report()

        # Действие
        report.create(reposity.data[data_reposity.group_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.group_key()}.md"
        self.__save_file(file_name, report.result)



    def test_md_report_create_receipt(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()

        report = markdown_report()

        # Действие
        report.create(reposity.data[data_reposity.receipt_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.receipt_key()}.md"
        self.__save_file(file_name, report.result)

    """
    JSON
    """
    def test_json_report_create_range(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()

        report = json_report()

        # Действие
        report.create(reposity.data[data_reposity.range_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.range_key()}.json"
        self.__save_file(file_name, report.result)



    def test_json_report_create_nomenclature(self):
        # Подготовка
        
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()

        report = json_report()

        # Действие
        report.create(reposity.data[data_reposity.nomenclature_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.nomenclature_key()}.json"
        self.__save_file(file_name, report.result)

    
    
    def test_json_report_create_group(self):
        # Подготовка
        
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()

        report = json_report()

        # Действие
        report.create(reposity.data[data_reposity.group_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.group_key()}.json"
        self.__save_file(file_name, report.result)

    
    
    def test_json_report_create_receipt(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()

        report = json_report()

        # Действие
        report.create(reposity.data[data_reposity.receipt_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.receipt_key()}.json"
        self.__save_file(file_name, report.result)

    """
    XML
    """
    def test_xml_report_create_range(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()

        report = xml_report()

        # Действие
        report.create(reposity.data[data_reposity.range_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.range_key()}.xml"
        self.__save_file(file_name, report.result)


    
    
    def test_xml_report_create_nomenclature(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()

        report = xml_report()

        # Действие
        report.create(reposity.data[data_reposity.nomenclature_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.nomenclature_key()}.xml"
        self.__save_file(file_name, report.result)



    def test_xml_report_create_group(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()

        report = xml_report()

        # Действие
        report.create(reposity.data[data_reposity.group_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.group_key()}.xml"
        self.__save_file(file_name, report.result)

    
    
    def test_xml_report_create_receipt(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()

        report = xml_report()

        # Действие
        report.create(reposity.data[data_reposity.receipt_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.receipt_key()}.xml"
        self.__save_file(file_name, report.result)


    """
    RTF
    """
    def test_rtf_report_create_range(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()

        report = rtf_report()

        # Действие
        report.create(reposity.data[data_reposity.range_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.range_key()}.rtf"
        self.__save_file(file_name, report.result)


    
    def test_rtf_report_create_nomenclature(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()

        report = rtf_report()

        # Действие
        report.create(reposity.data[data_reposity.nomenclature_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.nomenclature_key()}.rtf"
        self.__save_file(file_name, report.result)

    
    
    def test_rtf_report_create_group(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()

        report = rtf_report()

        # Действие
        report.create(reposity.data[data_reposity.group_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.group_key()}.rtf"
        self.__save_file(file_name, report.result)


    def test_rtf_report_create_receipt(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()

        report = rtf_report()

        # Действие
        report.create(reposity.data[data_reposity.receipt_key()])

        # Проверка
        print(report.result)
        assert report.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.receipt_key()}.rtf"
        self.__save_file(file_name, report.result)

   
