from Src.Services.start_service import start_service
from Src.data_reposity import data_reposity
from Src.Reports.csv_report import csv_report
from Src.Reports.xml_report import xml_report
from Src.Reports.json_report import json_report
from Src.Reports.rtf_report import rtf_report
from Src.Reports.markdown_report import markdown_report
from Src.Reports.report_factory import report_factory
from Src.Core.format_reporting import format_reporting
from Src.Managers.settings_manager import settings_manager

from Src.Reports.json_deserializer import json_deserializer
from Src.Models.range import range_model
from Src.Models.nomenclature import nomenclature_model
from Src.Models.receipt import receipt_model
from Src.Models.group import group_model

import unittest
import os


"""
Набор тестов для проверки работы формирование отчетов
"""
class test_reporting(unittest.TestCase):
    
    # Подготовка
    report_csv = csv_report()
    report_md = markdown_report()
    report_json = json_report()
    report_xml = xml_report()
    report_rtf = rtf_report()
    
    reposity = data_reposity()
    start = start_service(reposity)
    start.create()
    
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

        # Действие
        self.report_csv.create(self.reposity.data[ data_reposity.range_key()  ])

        # Проверки
        assert self.report_csv.result != ""
        
        self.__check_folder_exists()
        file_name = f"{data_reposity.range_key()}.csv"
        self.__save_file(file_name, self.report_csv.result)


    def test_csv_report_create_nomenclature(self):
        # Действие
        self.report_csv.create(self.reposity.data[ data_reposity.nomenclature_key()  ])

        # Проверки
        assert self.report_csv.result != "" 
        
        self.__check_folder_exists()
        file_name = f"{data_reposity.nomenclature_key()}.csv"
        self.__save_file(file_name, self.report_csv.result)  
        
        
    def test_csv_report_create_group(self):
        # Действие
        self.report_csv.create(self.reposity.data[data_reposity.group_key()])

        # Проверка
        assert self.report_csv.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.group_key()}.csv"
        self.__save_file(file_name, self.report_csv.result) 
        
        
    def test_csv_report_create_receipt(self):
        # Действие
        self.report_csv.create(self.reposity.data[data_reposity.receipt_key()])

        # Проверка
        assert self.report_csv.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.receipt_key()}.csv"
        self.__save_file(file_name, self.report_csv.result)
        
        
    """
    MARKDOWN
    """
    def test_md_report_create_range(self):
        # Действие
        self.report_md.create(self.reposity.data[data_reposity.range_key()])

        # Проверка
        assert self.report_md.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.range_key()}.md"
        self.__save_file(file_name, self.report_md.result)

   
    def test_md_report_create_nomenclature(self):
        # Действие
        self.report_md.create(self.reposity.data[data_reposity.nomenclature_key()])

        # Проверка
        assert self.report_md.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.nomenclature_key()}.md"
        self.__save_file(file_name, self.report_md.result)

    
    def test_md_report_create_group(self):
        # Действие
        self.report_md.create(self.reposity.data[data_reposity.group_key()])

        # Проверка
        assert self.report_md.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.group_key()}.md"
        self.__save_file(file_name, self.report_md.result)


    def test_md_report_create_receipt(self):
        # Действие
        self.report_md.create(self.reposity.data[data_reposity.receipt_key()])

        # Проверка
        assert self.report_md.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.receipt_key()}.md"
        self.__save_file(file_name, self.report_md.result)


    """
    JSON
    """
    def test_json_report_create_range(self):
        # Действие
        self.report_json.create(self.reposity.data[data_reposity.range_key()])

        # Проверка
        assert self.report_json.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.range_key()}.json"
        self.__save_file(file_name, self.report_json.result)


    def test_json_report_create_nomenclature(self):
        # Действие
        self.report_json.create(self.reposity.data[data_reposity.nomenclature_key()])

        # Проверка
        assert self.report_json.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.nomenclature_key()}.json"
        self.__save_file(file_name, self.report_json.result)

    
    def test_json_report_create_group(self):
        # Действие
        self.report_json.create(self.reposity.data[data_reposity.group_key()])

        # Проверка
        assert self.report_json.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.group_key()}.json"
        self.__save_file(file_name, self.report_json.result)

    
    def test_json_report_create_receipt(self):
        # Действие
        self.report_json.create(self.reposity.data[data_reposity.receipt_key()])
        
        # Проверка
        assert self.report_json.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.receipt_key()}.json"
        self.__save_file(file_name, self.report_json.result)


    """
    XML
    """
    def test_xml_report_create_range(self):
        # Действие
        self.report_xml.create(self.reposity.data[data_reposity.range_key()])

        # Проверка
        assert self.report_xml.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.range_key()}.xml"
        self.__save_file(file_name, self.report_xml.result)

    
    def test_xml_report_create_nomenclature(self):
        # Действие
        self.report_xml.create(self.reposity.data[data_reposity.nomenclature_key()])

        # Проверка
        assert self.report_xml.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.nomenclature_key()}.xml"
        self.__save_file(file_name, self.report_xml.result)


    def test_xml_report_create_group(self):
        # Действие
        self.report_xml.create(self.reposity.data[data_reposity.group_key()])

        # Проверка
        assert self.report_xml.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.group_key()}.xml"
        self.__save_file(file_name, self.report_xml.result)
    
    
    def test_xml_report_create_receipt(self):
        # Действие
        self.report_xml.create(self.reposity.data[data_reposity.receipt_key()])

        # Проверка
        assert self.report_xml.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.receipt_key()}.xml"
        self.__save_file(file_name, self.report_xml.result)


    """
    RTF
    """
    def test_rtf_report_create_range(self):
        # Действие
        self.report_rtf.create(self.reposity.data[data_reposity.range_key()])

        # Проверка
        assert self.report_rtf.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.range_key()}.rtf"
        self.__save_file(file_name, self.report_rtf.result)

    
    def test_rtf_report_create_nomenclature(self):
        # Действие
        self.report_rtf.create(self.reposity.data[data_reposity.nomenclature_key()])

        # Проверка
        assert self.report_rtf.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.nomenclature_key()}.rtf"
        self.__save_file(file_name, self.report_rtf.result)

    
    def test_rtf_report_create_group(self):
        # Действие
        self.report_rtf.create(self.reposity.data[data_reposity.group_key()])

        # Проверка
        assert self.report_rtf.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.group_key()}.rtf"
        self.__save_file(file_name, self.report_rtf.result)


    def test_rtf_report_create_receipt(self):
        # Действие
        self.report_rtf.create(self.reposity.data[data_reposity.receipt_key()])

        # Проверка
        assert self.report_rtf.result != ""

        self.__check_folder_exists()
        file_name = f"{data_reposity.receipt_key()}.rtf"
        self.__save_file(file_name, self.report_rtf.result)
        
        
        
    """
    Проверка работы отчета json для group
    """ 
    # def test_des_json_group(self):
    #     # Подготовка
    #     self.__test_json_report_create_group()
    #     file_name = "group_model.json"
    #     deserializer = json_deserializer(group_model)
    #     group_data = self.reposity.data[data_reposity.group_key()]

    #     # Действие
    #     deserializer.open(file_name)

    #     # Проверка
    #     assert len(deserializer.model_objects) != 0

    #     for object, data in zip(deserializer.model_objects, group_data):
    #         assert object == data

    #     assert deserializer.model_objects[1] != group_data[0]


    # """
    # Проверка десериализации данных из JSON для range
    # """
    # def test_des_json_range(self):
    #     # Подготовка
    #     self.__test_json_report_create_range()
    #     file_name = "range_model.json"
    #     deserializer = json_deserializer(range_model)
    #     range_data = self.reposity.data[data_reposity.range_key()]

    #     # Действие
    #     deserializer.open(file_name)

    #     # Проверка
    #     assert len(deserializer.model_objects) != 0

    #     for object, data in zip(deserializer.model_objects, range_data):
    #         assert object == data

    #     assert deserializer.model_objects[1] != range_data[0]

    
    # """
    # Проверка десериализации данных из JSON для nomenclature
    # """
    # def test_des_json_nomenclature(self):
    #     # Подготовка
    #     self.__test_json_report_create_nomenclature()
    #     file_name = "nomenclature_model.json"
    #     deserializer = json_deserializer(nomenclature_model)
    #     nomenclature_data = self.reposity.data[data_reposity.nomenclature_key()]

    #     # Действие
    #     deserializer.open(file_name)

    #     # Проверка
    #     assert len(deserializer.model_objects) != 0

    #     for object, data in zip(deserializer.model_objects, nomenclature_data):
    #         assert object == data

    #     assert deserializer.model_objects[1] != nomenclature_data[0] 

    # """
    # Проверка десериализации данных из JSON для recipe
    # """
    # def test_des_json_recipe(self):
    #     # Подготовка
    #     self.__test_json_report_create_receipt
    #     file_name = "receipt_model.json"
    #     deserializer = json_deserializer(receipt_model)
    #     recipe_data = self.reposity.data[data_reposity.receipt_key()]

    #     # Действие
    #     deserializer.open(file_name)

    #     # Проверка
    #     assert len(deserializer.model_objects) != 0

    #     for object, data in zip(deserializer.model_objects, recipe_data): 
    #         assert object == data

    #     assert deserializer.model_objects[1] != recipe_data[0]

   
