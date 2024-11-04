from Src.Core.validator import validator
from Src.Core.format_transaction import format_transaction


class calculations:


    def __init__(self, _type: format_transaction):
        validator.validate(_type, format_transaction)
        self.transaction = getattr(self, _type.name.lower())


    def income(self, turnover: float, quantity: float) -> float:
        validator.validate(turnover, float)
        validator.validate(quantity, float)

        result = turnover + quantity
        return result
    
    
    def expenditure(self, turnover: float, quantity: float) -> float:
        validator.validate(turnover, float)
        validator.validate(quantity, float)

        result = turnover - quantity
        return result