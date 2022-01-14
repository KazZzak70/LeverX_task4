from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from courses.views import (
    RegisterView,
    CourseView,
    CourseDetailView,
    CourseMemberView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('courses/<int:course_id>/', CourseDetailView.as_view(), name='detail_course'),
    path('courses/', CourseView.as_view(), name='list_courses'),
    path('coursemembers/<int:course_id>/', CourseMemberView.as_view(), name='course_members'),
]
