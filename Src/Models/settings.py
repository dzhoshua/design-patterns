from Src.Core.validator import validator


"""
Настройки
"""
class settings:
    __organization_name = ""
    __inn = ""

    """
    Наименование организации
    """
    @property
    def organization_name(self):
        return self.__organization_name
    

    @organization_name.setter
    def organization_name(self, value:str):
        validator.validate(value, str, 255)
        self.__organization_name = value

    """
    ИНН
    """
    @property
    def inn(self):
        return self.__inn

    def inn(self, value:str):
        validator.validate(value, str, 9)
        self.__inn = value

