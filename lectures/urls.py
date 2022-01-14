from django.urls import path
from lectures.views import (
    LectureDetailView,
    LectureCreateView,
    HometaskView,
    SolutionListView,
)

urlpatterns = [
    path('lectures/<int:lecture_id>/', LectureDetailView.as_view()),
    path('lectures/', LectureCreateView.as_view()),
    path('hometasks/', HometaskView.as_view()),
    path('solutions/', SolutionListView.as_view()),
]
