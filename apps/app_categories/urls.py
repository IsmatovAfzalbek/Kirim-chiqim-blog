from django.urls import path

from . import views




urlpatterns = [
    path('list/', views.CategoryListCreateView.as_view(), name='category-list'),
    path('detail/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
]