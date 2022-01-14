from django.urls import path
from reports.views import (
    CommentCreateView,
    ReportsListView,
    ReportDetailView,
)

urlpatterns = [
    path('reports/<int:report_id>/', ReportDetailView.as_view()),
    path('reports/', ReportsListView.as_view()),
    path('comments/', CommentCreateView.as_view()),
]
