from Src.Core.abstract_logic import abstract_logic


class data_repository(abstract_logic):
    __data = []
    
    def __new__(cls):
        if not isinstance(str):
            pass
    
    @property
    def data(self):
        return self.__data
    
    """
    ключ для хранения групп номенклатуры
    """
    @staticmethod
    def group_key() -> str:
        return "group"