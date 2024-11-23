from Src.Core.abstract_logic import abstract_logic
from Src.settings import settings
from Src.Managers.settings_manager import settings_manager
from Src.Core.event_type import event_type
from Src.data_reposity import data_reposity
from Src.Core.validator import operation_exception, validator
from Src.Models.group import group_model
from Src.Models.range import range_model
from Src.Models.nomenclature import nomenclature_model
from Src.Models.receipt import receipt_model
from Src.Models.ingredient import ingredient_model

from Src.Models.warehouse import warehouse_model
from Src.Models.warehouse_transaction import warehouse_transaction
from Src.Core.format_transaction import format_transaction
from Src.Services.observe_service import observe_service

from datetime import datetime, timedelta
import random

"""
Сервис для реализации первого старта приложения
"""
class start_service(abstract_logic):
    __reposity: data_reposity = None
    __nomenclatures:dict = {}
    __settings_manager: settings_manager = None


    def __init__(self, reposity: data_reposity, manager: settings_manager) -> None:
        super().__init__()
        validator.validate(reposity, data_reposity)
        self.__reposity = reposity
        self.__settings_manager = manager
        
        
    def handle_event(self, type: event_type, params):
        return super().handle_event(type, params)
    
    
    @property 
    def settings(self) -> settings:
        return self.__settings_manager.settings
    

    """
    Сформировать стартовый набор групп номенклатуры
    """
    def __create_nomenclature_groups(self):
        items = [group_model.default_group_source(), group_model.default_group_cold()]
        self.__reposity.data[data_reposity.group_key()] = items    


    """
    Получить Default набор данных 
    """
    def __get_default_items(self):
        group_list = list(filter(lambda x: x.name == "Сырье", self.__reposity.data[data_reposity.group_key()]  ))
        if len(group_list) == 0:
            raise operation_exception(f"В стартовом наборе default группа 'Сырье'  не найдена!")
        group = group_list[0]
        
        base_gramm_list = list(filter(lambda x: x.name == "грамм", self.__reposity.data[data_reposity.range_key()]  ))
        if len(base_gramm_list) == 0:
            raise operation_exception(f"В стартовом наборе default единица измерения 'грамм'  не найдена!")
        base_gramm = base_gramm_list[0]
        
        base_item_list = list(filter(lambda x: x.name == "штука", self.__reposity.data[data_reposity.range_key()]  ))
        if len(base_item_list) == 0:
            raise operation_exception(f"В стартовом наборе default единица измерения 'штука'  не найдена!")
        base_item = base_item_list[0]

        base_killogram_list = list(filter(lambda x: x.name == "кг", self.__reposity.data[data_reposity.range_key()]  ))
        if len(base_killogram_list) == 0:
            raise operation_exception(f"В стартовом наборе default единица измерения 'кг'  не найдена!")
        base_killogram = base_killogram_list[0]

        return (group, base_gramm, base_item, base_killogram)


    """
    Сформировать стартовый набор номенклатуры
    """
    def __create_nomenclatures(self):
        # Формируем словарь для дальнейшего переиспользования
        default = self.__get_default_items()
        self.__nomenclatures["Пшеничная мука"] = [nomenclature_model.create("Пшеничная мука", default[3], default[0] ), 100]
        self.__nomenclatures["Сахар"] = [nomenclature_model.create("Сахар", default[3], default[0] ), 80]
        self.__nomenclatures["Сливочное масло"] = [nomenclature_model.create("Сливочное масло", default[3], default[0] ),70]
        self.__nomenclatures["Яйцо"] = [nomenclature_model.create("Яйцо", default[2], default[0] ), 1]
        self.__nomenclatures["Ванилин"] = [nomenclature_model.create("Ванилин", default[3], default[0] ), 5]

        # Формируем список номенклатуры
        items = []
        for value in self.__nomenclatures.values():
            items.append(value[0])

        self.__reposity.data[data_reposity.nomenclature_key()] = items



    """
    Сформировать стартовый набор единиц измерения
    """
    def __create_ranges(self):
        base_gramm = range_model.create("грамм", 1)
        base_ml = range_model.create("миллилитр", 1)
        base_item = range_model.create("штука", 1)

        items = [base_gramm, base_ml, range_model.create("кг", 1000, base_gramm), range_model.create("литр", 1000, base_ml), base_item ]  
        self.__reposity.data[data_reposity.range_key()] = items


    """
    Сформировать стартовый набор рецепты
    """
    def __create_receipts(self):
        # Формируем список ингредиентов
        ingredients = []
        for value in self.__nomenclatures.values():
            base_range = value[0].range.base or value[0].range
            ingredient = ingredient_model.create(value[0], base_range, value[1])
            ingredients.append(ingredient)

        # Формируем рецепты
        receipt =  receipt_model.create("Вафли хрустящие в вафельнице", ingredients, 
                                        ["Подготовьте необходимые продукты. Из данного количества у меня получилось 8 штук диаметром около 10 см.",
                                         "Масло положите в сотейник с толстым дном. Растопите его на маленьком огне на плите, на водяной бане либо в микроволновке.",
                                         "Добавьте в теплое масло сахар. Перемешайте венчиком до полного растворения сахара. От тепла сахар довольно быстро растает.",
                                         "Добавьте в масло яйцо. Предварительно все-таки проверьте масло, не горячее ли оно, иначе яйцо может свариться. Перемешайте яйцо с маслом до однородности.",
                                         "Всыпьте муку, добавьте ванилин.",
                                         "Перемешайте массу венчиком до состояния гладкого однородного теста.",
                                         "Разогрейте вафельницу по инструкции к ней. У меня очень старая, еще советских времен электровафельница. Она может и не очень красивая, но печет замечательно!",
                                         "Пеките вафли несколько минут до золотистого цвета. Осторожно откройте вафельницу, она очень горячая! Снимите вафлю лопаткой. Горячая она очень мягкая, как блинчик."],
                                         10, 10)
                                        
        self.__reposity.data[data_reposity.receipt_key()] = [receipt]  
        
    
    """
    Сформировать склады
    """    
    def __create_warehouse(self):
        # Формируем склад
        warehouses = [
            warehouse_model.create("Склад1", "ул. Баумана 222"),
            warehouse_model.create("Склад2", "ул. Ленина 111")
            ]
        self.__reposity.data[data_reposity.warehouse_key()] = warehouses
    
    
    """
    Сформировать транзакции
    """    
    def __create_transaction(self):
        # Формируем транзакции
        count = 100
        transactions = []
        warehouses = self.__reposity.data[data_reposity.warehouse_key()]
        nomenclatures = self.__reposity.data[data_reposity.nomenclature_key()]
        
        count_iter = count // len(nomenclatures)
        for i in range(count_iter):
            for nomenclature in nomenclatures:
                range1 = nomenclature.range
                date = datetime.now() - timedelta(days=random.randint(0, 365))
                random_quantity = random.randint(10, 300)
                random_transaction_type = random.choice(list(format_transaction)) 
                random_warehouse = random.choice(warehouses)

                transaction = warehouse_transaction.create(
                    random_warehouse,
                    nomenclature,
                    range1,
                    float(random_quantity),
                    random_transaction_type,
                    date 
                )
                transactions.append(transaction)
            
        self.__reposity.data[data_reposity.transaction_key()] = transactions
     

    """
    Первый старт
    """
    def create(self) -> bool:
        try:
            if self.settings.first_start:
                self.__create_nomenclature_groups()
                self.__create_ranges()
                self.__create_nomenclatures()
                self.__create_receipts()
                
                self.__create_warehouse()
                self.__create_transaction()
                
                observe_service.raise_event(event_type.DEBUG, "Первый старт сервиса.")
            else:
                observe_service.raise_event(event_type.DEBUG, "Первый старт сервиса.")
                observe_service.raise_event(event_type.RESTORE_DATA_REPOSITY, {})
            return True
        except Exception as ex:
            self.set_exception(ex)
            return False    

    """
    Перегрузка абстрактного метода
    """
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex) 