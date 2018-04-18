from django.urls import path
from downloader.youtube import views

urlpatterns = (
    path('', views.link_enter_page, name='enter-link'),
    path('success/', views.success_page, name='success'),
)
