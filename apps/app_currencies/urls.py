from django.urls import path

from . import views


urlpatterns = [
    path('list/', views.CurrencyListCreateView.as_view(), name='currency-list'),
    path('detail/<int:pk>/', views.CurrencyDetailView.as_view(), name='currency-detail'),
    path('rates/fetch/', views.FetchRateView.as_view(), name='fetch-rate'),
]