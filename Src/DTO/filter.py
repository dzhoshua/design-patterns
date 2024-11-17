from Src.Core.validator import validator, argument_exception
from Src.Core.format_filter import format_filter
from datetime import datetime


class filter:
    __name: str = ""
    __filter_name = format_filter.EQUALS
    
    __unique_code: str = ""
    __filter_unique_code = format_filter.EQUALS
    
    __period: list[datetime] = None
    

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, name: str):
        if name:
            validator.validate(name, str)
        self.__name = name
        

    @property
    def filter_name(self) -> format_filter:
        return self.__filter_name
    
    @filter_name.setter
    def filter_name(self, value: format_filter):
        validator.validate(value, format_filter)
        self.__filter_name = value


    @property
    def unique_code(self) -> str:
        return self.__unique_code
    
    @unique_code.setter
    def unique_code(self, value: str):
        if value:
            validator.validate(value, str)
        self.__unique_code = value


    @property
    def filter_unique_code(self) -> format_filter:
        return self.__filter_unique_code
    
    @filter_unique_code.setter
    def filter_unique_code(self, value: format_filter):
        validator.validate(value, format_filter)
        self.__filter_unique_code = value
        
        
    @property
    def period(self) -> list:
        return self.__period
    
    @period.setter
    def period(self, value: list):
        validator.validate(value, list)
        if len(value) == 2:
            validator.validate(value[0], datetime)
            validator.validate(value[1], datetime)
            if value[0] >= value[1]:
                raise argument_exception(f"Дата start_period должна быть меньше end_period.")
        self.__period = value


    @staticmethod
    def create(data: dict) -> filter:
        validator.validate(data, dict)
        
        filter_name = data.get('filter_name', format_filter.EQUALS.value).upper()
        filter_unique_code = data.get('filter_unique_code', format_filter.EQUALS.value).upper()
        filter_name = getattr(format_filter, filter_name)
        filter_unique_code = getattr(format_filter, filter_unique_code)

        filter_ = filter()
        filter_.name = data.get('name', "")
        filter_.unique_code = data.get('unique_code', "")
        filter_.filter_name = filter_name
        filter_.filter_unique_code = filter_unique_code
        
        start_period = data.get('start_period', "")
        end_period = data.get('end_period', "")
        filter_.period = []
        if start_period and end_period:
            start_period = datetime.strptime(start_period, "%Y-%m-%d")
            end_period = datetime.strptime(end_period, "%Y-%m-%d")
            filter_.period = [start_period, end_period]
        
        return filter_
    
    def __str__(self) -> str:
        return f"Filter(\nname: {self.name}\nfilter_name: {self.filter_name}\nunique_code: {self.unique_code}\nfilter_unique_code: {self.filter_unique_code}\n)"