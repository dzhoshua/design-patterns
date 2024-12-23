from Src.Core.abstract_logic import abstract_logic
from Src.Core.validator import argument_exception
from Src.Core.event_type import event_type


""""
Наблюдатель
"""
class observe_service:
    observers = []

    @staticmethod
    def append(service: abstract_logic):

        if service is None:
            return

        if not isinstance(service, abstract_logic):
            raise argument_exception("Некорректный тип данных!")

        items =  list(map( lambda x: type(x).__name__,  observe_service.observers))
        found =    type( service ).__name__ in items 
        if not found: 
            observe_service.observers.append( service )

    @staticmethod
    def raise_event( type_: event_type, params):
        result = {}
        for instance in observe_service.observers:
            if instance is not None:
                class_name = type(instance).__name__
                value = instance.handle_event( type_, params)  
                result[class_name] = value
        return result