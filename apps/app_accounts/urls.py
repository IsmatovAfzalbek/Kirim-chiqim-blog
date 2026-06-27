from django.urls import path

from . import views





urlpatterns = [
    path('list/', views.ListCreateView.as_view(), name='account-list'),
    path('detail/<int:pk>/', views.AccountDetail.as_view(), name='account-detail'),
]