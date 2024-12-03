from typing import Any

from sqlalchemy.future import select

from db.base import Base
from managers.mixins import SQLAlchemyMultipleExpressionsBuilder
from managers.mixins.base_mixin import BaseMixin


class FilterMixin(BaseMixin):
    """
    Mixin to filter model rows
    """

    async def filter(self, *args, **kwargs) -> Base:
        """Return list of suitable for filters rows"""

        query = self._generate_query(*args, **kwargs)
        rows = await self.session.execute(query)
        return rows.scalars().all()

    async def filter_one(self, *args, **kwargs) -> Base:
        """Return first suitable for filters row"""

        query = self._generate_query(*args, **kwargs)
        rows = await self.session.execute(query)
        return rows.scalars().first()

    def _generate_query(self, *args, **kwargs):
        query = select(self.model_class)
        if args and type(args[0]) == SQLAlchemyMultipleExpressionsBuilder:
            builder = args[0]
            query = query.where(builder.generate(model_class=self.model_class))
        else:
            for searching_criteria, value in kwargs.items():
                searching_criteria = searching_criteria.split('__')
                lookup_field = searching_criteria[0]
                comparison_type = None if len(searching_criteria) == 1 else searching_criteria[1]
                query = self._update_query(
                    query=query,
                    lookup_field=lookup_field,
                    comparison_type=comparison_type,
                    value=value
                )
        return query

    def _update_query(self, query, lookup_field: str, comparison_type: str, value: Any):
        field = getattr(self.model_class, lookup_field)
        comparison_type_map = {
            None: lambda _value: field.__eq__(_value),
            'ne': lambda _value: field.__ne__(_value),
            'in': lambda _value: field.in_(_value),
            'contains': lambda _value: field.contains([_value])
        }
        return query.where(comparison_type_map[comparison_type](value))
