from django_filters import rest_framework as filters

from worklogs.models import WorkLog

class WorkLogFilter(filters.FilterSet):
    work_date = filters.DateFromToRangeFilter()
    work_date_exact = filters.DateFilter(field_name='work_date', lookup_expr='exact')

    class Meta:
        model = WorkLog
        fields = ['work_date', 'work_date_exact','user', 'task']
