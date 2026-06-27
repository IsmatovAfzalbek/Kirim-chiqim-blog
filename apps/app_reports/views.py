from datetime import date, timedelta
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.app_transactions.models import Transaction





class DailyReportView(APIView):
    permission_classes = [IsAuthenticated]
    
    
    def get(self, request):
        today = request.query_params.get("date", date.today())
        transactions = Transaction.objects.filter(user = request.user, date = today)
        
        income = transactions.filter(
            transaction_type = "income"
            ).aggregate(total = Sum("amount_uzs"))["total"] or 0
        
        expense = transactions.filter(
            transaction_type="expense"
            ).aggregate(total = Sum("amount_uzs"))["total"] or 0
        
        balance = income - expense
        
        return Response({
                "date": today,
                "income": income,
                "expense": expense,
                "balance": balance
            }, status=status.HTTP_200_OK)
        
        
        
class WeeklyReportView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
   
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        transactions = Transaction.objects.filter(
                user=request.user,
                date__gte=start_of_week,
                date__lte=end_of_week
            )

        income = transactions.filter(
            transaction_type='income'
        ).aggregate(total=Sum('amount_uzs'))['total'] or 0

        expense = transactions.filter(
            transaction_type='expense'
        ).aggregate(total=Sum('amount_uzs'))['total'] or 0

        balance = income - expense

        return Response({
            "start_of_week": start_of_week,
            "end_of_week": end_of_week,
            "income": income,
            "expense": expense,
            "balance": balance
        }, status=status.HTTP_200_OK)



class MonthlyReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = date.today()
        year = int(request.query_params.get('year', today.year))
        month = int(request.query_params.get('month', today.month))

        transactions = Transaction.objects.filter(
            user=request.user,
            date__year=year,
            date__month=month
        )

        income = transactions.filter(
            transaction_type='income'
        ).aggregate(total=Sum('amount_uzs'))['total'] or 0

        expense = transactions.filter(
            transaction_type='expense'
        ).aggregate(total=Sum('amount_uzs'))['total'] or 0

        balance = income - expense

        return Response({
            "year": year,
            "month": month,
            "income": income,
            "expense": expense,
            "balance": balance
        }, status=status.HTTP_200_OK)
        
        
        
class YearlyReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = date.today()
        year = int(request.query_params.get('year', today.year))

        transactions = Transaction.objects.filter(
            user=request.user,
            date__year=year
        )

        income = transactions.filter(
            transaction_type='income'
        ).aggregate(total=Sum('amount_uzs'))['total'] or 0

        expense = transactions.filter(
            transaction_type='expense'
        ).aggregate(total=Sum('amount_uzs'))['total'] or 0

        balance = income - expense

        return Response({
            "year": year,
            "income": income,
            "expense": expense,
            "balance": balance
        }, status=status.HTTP_200_OK)













