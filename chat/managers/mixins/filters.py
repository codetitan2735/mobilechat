from sqlalchemy import and_, or_, not_

from db.base import Base


class SQLAlchemyMultipleExpressionsBuilder:
    operation: str = None

    def __init__(self, operation: str, expressions: list):
        self.operation = operation
        self.expressions = expressions

    def generate(self, model_class: Base):
        operation_map = {
            'AND': and_,
            'OR': or_,
            'NOT': not_,
        }
        filter_objects = []
        for expression in self.expressions:
            field = getattr(model_class, expression['lookup_field'])
            comparison_type_map = {
                None: lambda _value: field.__eq__(_value),
                'ne': lambda _value: field.__ne__(_value),
                'in': lambda _value: field.in_(_value),
                'contains': lambda _value: field.contains(_value)
            }
            filter_objects.append(comparison_type_map[expression['comparison_type']](expression['value']))
        return operation_map[self.operation](*filter_objects)


class Q:
    filters = {}
    field = None

    def __init__(self, **kwargs):
        for searching_criteria, value in kwargs.items():
            searching_criteria = searching_criteria.split('__')
            lookup_field = searching_criteria[0]
            comparison_type = None if len(searching_criteria) == 1 else searching_criteria[1]
            self.filters = {
                'lookup_field': lookup_field,
                'comparison_type': comparison_type,
                'value': value
            }
            break

    def __and__(self, other: 'Q') -> SQLAlchemyMultipleExpressionsBuilder:
        return SQLAlchemyMultipleExpressionsBuilder(operation='AND', expressions=[self.filters, other.filters])

    def __or__(self, other: 'Q') -> SQLAlchemyMultipleExpressionsBuilder:
        return SQLAlchemyMultipleExpressionsBuilder(operation='OR', expressions=[self.filters, other.filters])

    def __invert__(self):
        return SQLAlchemyMultipleExpressionsBuilder(operation='NOT', expressions=[self.filters])
