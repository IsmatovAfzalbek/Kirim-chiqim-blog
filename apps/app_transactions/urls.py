from django.urls import path

from . import views





urlpatterns = [
    path('list/', views.TransactionListCreateView.as_view(), name='transaction-list'),
    path('detail/<int:pk>/', views.TransactionDetailView.as_view(), name='transaction-detail'),
    path('recurring/list/', views.RecurringTransactionListCreateView.as_view(), name='recurring-list'),
    path('recurring/detail/<int:pk>/', views.RecurringTransactionDetailView.as_view(), name='recurring-detail'),
]