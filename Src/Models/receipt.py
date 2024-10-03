from Src.Core.validator import argument_exception, validator
from Src.Models.ingredient import ingredient_model
from Src.Core.base_models import  base_model_name

"""
Модель рецепта
"""
class receipt_model(base_model_name):
    # Ингредиенты
    __ingredients: dict = {}

    # Инструкции
    __instructions: list[str]

    # Время приготовления одной порции (мин)
    __cooking_period:int

    # Количество порций
    __cooking_portion:int

   
    """
    Ингредиенты
    """
    @property
    def ingredients(self) -> dict:
        return self.__ingredients
    
    @ingredients.setter
    def ingredients(self, value: dict):
        validator.validate(value, dict)
        self.__ingredients = value


    """
    Количество порций
    """
    @property
    def cooking_portion(self) -> int:
        return self.__cooking_portion    
    
    @cooking_portion.setter
    def cooking_portion(self, value: int):
        validator.validate(value, int)
        self.__cooking_portion = value
        
    

    """
    Инструкции по приготовления
    """
    @property
    def instructions(self) -> list[str]:
        return self.__instructions
    
    @instructions.setter
    def instructions(self, value:list[str]):
        validator.validate(value, list)
        self.__instructions = value
    
    """
    Время приготовления
    """
    @property
    def cooking_period(self) -> int:
        return self.__cooking_period
    
    @cooking_period.setter
    def cooking_period(self, value:int):
        validator.validate(value, int)
        if value <= 0:
            raise argument_exception("Некорректный аргумент!")
        
        self.__cooking_period = value

    def to_dict(self):
        return {
            "unique_code": self.unique_code,
            "name": self.name,
            "cooking_period": self.cooking_period,
            "cooking_portion": self.cooking_portion,
            "ingredients": self.ingredients,
            "instructions": self.instructions
        }
    """
    Фабричный метод
    """
    @staticmethod
    def create(name: str, ingredients: dict, insructions:list[str], cooking_period:int, cooking_portion:int )  :
        validator.validate(name, str)
        if len(ingredients) == 0:
            raise argument_exception("Некорректный аргумент!")

        item = receipt_model()
        item.name = name
        item.cooking_period = cooking_period
        item.instructions = insructions
        item.ingredients = ingredients
        item.cooking_portion = cooking_portion
        return item