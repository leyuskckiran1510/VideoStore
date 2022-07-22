from django.contrib import admin
from django.urls import path, include
from django.conf.urls import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('video.urls')),
]

urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)