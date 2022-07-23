from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.video_new, name='upload'),
    path('charge/', views.charge, name='charge'),
    path('list/', views.video_list, name='list'),
    path('vapi/list', views.video_list_json, name='list_json'),
    path('list/<str:date>', views.video_list, name='list_detail'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout', views.logout_view, name='logout'),
    path('accounts/signup', views.signup, name='signup'),
    path('vapi/<str:year>/<str:month>/<str:day>/<str:filename>', views.video_dump, name='return'),
    path('vapi/<str:year>/<str:month>/<str:day>', views.video_dump, name='return'),
    path('vapi/<str:year>/<str:month>', views.video_dump, name='return'),
    path('vapi/<str:year>', views.video_dump, name='return'),



]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

