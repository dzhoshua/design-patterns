from Src.Core.base_models import base_model_name

"""
Модель группы номенклатуры
"""
class group_model(base_model_name):

    """
    Фабричный метод
    """
    # @staticmethod
    # def create(name: str) -> 'group_model':
    #     item = group_model()
    #     item.name = name
    #     return item
    
    def to_dict(self):
        return {
            "unique_code": self.unique_code,
            "name": self.name
        }
    @staticmethod
    def default_group_source():
        item = group_model()
        item.name = "Сырье"
        return item
    
    @staticmethod
    def default_group_cold():
        item = group_model()
        item.name = "Заморозка"
        return item
    

    


    
