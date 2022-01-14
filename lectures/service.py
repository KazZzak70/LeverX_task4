from django_filters import rest_framework as filters
from lectures.models import Solution


class SolutionFilter(filters.FilterSet):
    task = filters.BaseInFilter

    class Meta:
        model = Solution
        fields = ["task", ]
