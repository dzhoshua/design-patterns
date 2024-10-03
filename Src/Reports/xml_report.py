from Src.Core.format_reporting import format_reporting
from Src.Core.abstract_report import abstract_report
from Src.Core.validator import validator, operation_exception
import xml.etree.ElementTree as ET
from xml.dom import minidom



class xml_report(abstract_report):

    def __init__(self) -> None:
       super().__init__()
       self.__format = format_reporting.XML

 
    def create(self, data: list):
        validator.validate(data, list)
        if len(data) == 0:
            raise operation_exception("Набор данных пуст!")
        

        first_model = data[0]
        fields = list(filter(lambda x: not x.startswith("_") and not callable(getattr(first_model.__class__, x)), dir(first_model) ))
        root = ET.Element("report")
        
        # Данные
        for row in data:
            row_element = ET.SubElement(root, "item")
            for field in fields:
                value = getattr(row, field)
                
                value = self.__serialize(value)
                
                field_element = ET.SubElement(row_element, field)
                field_element.text = str(value) if value is not None else ""
        
        raw_xml = ET.tostring(root, encoding="unicode", method="xml")

        parsed_xml = minidom.parseString(raw_xml)
        self.result = parsed_xml.toprettyxml(indent="    ")
        
    def __serialize(self, value):
        if isinstance(value, list):
            return [self.__serialize(item) for item in value]
        if isinstance(value, dict):
            return {key: self.__serialize(val) for key, val in value.items() if not key.startswith("_")}
        elif hasattr(value, "to_dict"):
            return value.to_dict()
        elif hasattr(value, "__dict__"):
            return {key: self.__serialize(val) for key, val in value.__dict__.items() if not key.startswith("_")}
        else:
            return value