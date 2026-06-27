from django.urls import path

from . import views




urlpatterns = [
    path('daily/', views.DailyReportView.as_view(), name='daily-report'),
    path('weekly/', views.WeeklyReportView.as_view(), name='weekly-report'),
    path('monthly/', views.MonthlyReportView.as_view(), name='monthly-report'),
    path('yearly/', views.YearlyReportView.as_view(), name='yearly-report'),
]