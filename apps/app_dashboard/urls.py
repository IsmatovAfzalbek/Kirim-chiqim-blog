from django.urls import path

from . import views




urlpatterns = [
    path('main/', views.DashboardView.as_view(), name='dashboard'),
]