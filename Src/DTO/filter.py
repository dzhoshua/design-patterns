from Src.Core.validator import validator
from Src.Core.format_filter import format_filter


class filter:
    __name: str = ""
    __filter_name = format_filter.EQUALS
    __unique_code: str = ""
    __filter_unique_code = format_filter.EQUALS

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, name: str):
        validator.validate(name, str)
        self.__name = name
        

    @property
    def filter_name(self) -> format_filter:
        return self.__filter_name
    
    @filter_name.setter
    def filter_name(self, filter_name: format_filter):
        validator.validate(filter_name, format_filter)
        self.__filter_name = filter_name


    @property
    def unique_code(self) -> str:
        return self.__unique_code
    
    @unique_code.setter
    def unique_code(self, unique_code: str):
        validator.validate(unique_code, str)
        self.__unique_code = unique_code


    @property
    def filter_unique_code(self) -> format_filter:
        return self.__filter_unique_code
    
    @filter_unique_code.setter
    def filter_unique_code(self, filter_unique_code: format_filter):
        validator.validate(filter_unique_code, format_filter)
        self.__filter_unique_code = filter_unique_code


    @staticmethod
    def create(data) -> filter:
        
        filter_name = data.get('filter_name').upper()
        filter_name = getattr(format_filter, filter_name)
        filter_unique_code = data.get('filter_unique_code').upper()
        filter_unique_code = getattr(format_filter, filter_unique_code)

        filter_ = filter()
        filter_.name = data.get('name')
        filter_.unique_code = data.get('unique_code')
        filter_.filter_name = filter_name
        filter_.filter_unique_code = filter_unique_code

        return filter_
    
    def __str__(self) -> str:
        return f"Filter(\nname: {self.name}\nfilter_name: {self.filter_name}\nunique_code: {self.unique_code}\nfilter_unique_code: {self.filter_unique_code}\n)"