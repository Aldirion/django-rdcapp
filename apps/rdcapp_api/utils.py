from django.db.models import PositiveIntegerField, Subquery, Aggregate


class SubqueryCount(Subquery):
    # Custom Count function to just perform simple count on any queryset without grouping.
    # https://stackoverflow.com/a/47371514/1164966
    template = "(SELECT count(*) FROM (%(subquery)s) _count)"
    output_field = PositiveIntegerField()  # type: ignore


class SubqueryAggregate(Subquery):
    # https://code.djangoproject.com/ticket/10060
    template = '(SELECT %(function)s(_agg."%(column)s") FROM (%(subquery)s) _agg)'
    contains_aggregate = True

    def __init__(self, queryset, column, output_field=None, **extra):
        if not output_field:
            # infer output_field from field type
            output_field = queryset.model._meta.get_field(column)
        super().__init__(
            queryset, output_field, column=column, function=self.function, **extra
        )


class SubquerySum(Subquery):
    template = "(SELECT SUM(%(column)s::integer) FROM (%(subquery)s) _agg)"
    output_field = PositiveIntegerField()


class Sum(Aggregate):
    # Supports SUM(ALL field).
    function = "SUM(text::int)"
    template = "%(function)s(%(all_values)s%(expressions)s)"
    allow_distinct = False

    def __init__(self, expression, all_values=False, **extra):
        super().__init__(expression, all_values="ALL " if all_values else "", **extra)
