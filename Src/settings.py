from Src.Core.validator import validator


"""
Настройки
"""
class settings:
    __organization_name = ""
    __inn = ""
    __account = ""
    __correspondent_account = ""
    __bic = ""
    __organization_type = ""

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
        validator.validate(value, str, 12)
        self.__inn = value
        
    
    """
    Счет
    """
    @property
    def account(self):
        return self.__account

    def account(self, value:str):
        validator.validate(value, str, 11)
        self.__account = value
        
    """
    Корреспондентский счет
    """
    @property
    def correspondent_account(self):
        return self.__correspondent_account

    def correspondent_account(self, value:str):
        validator.validate(value, str, 11)
        self.__correspondent_account = value
        
    
    """
    БИК
    """
    @property
    def bic(self):
        return self.__bic

    def bic(self, value:str):
        validator.validate(value, str, 9)
        self.__bic = value
        
        
    """
    Вид собственности
    """
    @property
    def organization_type(self):
        return self.__organization_type

    def organization_type(self, value:str):
        validator.validate(value, str, 5)
        self.__organization_type = value
    
