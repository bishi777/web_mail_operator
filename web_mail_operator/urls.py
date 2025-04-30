from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path
from app import views
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.IndexView.as_view(), name='index'),
    path('how_to_use/', views.how_to_use_view, name='how_to_use'), 
    path('terms_of_service/', views.terms_of_service_view, name='terms_of_service'), 
    path('api/', include(router.urls)),
    path('api/user-data/', views.UserDataView.as_view(), name='user-data'),
    path('api/user-data/<int:user_id>/', views.UserDataView.as_view(),),  # PATCHリクエスト用のURL
]
# 開発環境でメディアファイルを提供
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)