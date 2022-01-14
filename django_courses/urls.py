from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('api/v1/admin/', admin.site.urls),
    path('api/v1/', include('courses.urls')),
    path('api/v1/', include('lectures.urls')),
    path('api/v1/', include('reports.urls')),
]

urlpatterns.extend(doc_urls)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
