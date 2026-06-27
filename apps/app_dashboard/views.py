from datetime import date
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.app_transactions.models import Transaction, RecurringTransaction
from apps.app_transactions.serializers import TransactionSerializer
from apps.app_accounts.models import Account





class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = date.today()

        total_balance = Account.objects.filter(
            user=request.user
        ).aggregate(total=Sum('balance'))['total'] or 0

        monthly_transactions = Transaction.objects.filter(
            user=request.user,
            date__year=today.year,
            date__month=today.month
        )

        income = monthly_transactions.filter(
            transaction_type='income'
        ).aggregate(total=Sum('amount_uzs'))['total'] or 0

        expense = monthly_transactions.filter(
            transaction_type='expense'
        ).aggregate(total=Sum('amount_uzs'))['total'] or 0

        transactions = Transaction.objects.select_related(
            'user', 'account', 'category', 'currency'
        ).filter(user=request.user).order_by('-date')

        active_recurring = RecurringTransaction.objects.filter(
            user=request.user, is_active=True
        ).count()

        serializer = TransactionSerializer(transactions, many=True)

        return Response({
            "total_balance": total_balance,
            "monthly": {
                "income": income,
                "expense": expense,
                "balance": income - expense
            },
            "transactions": serializer.data,
            "active_recurring": active_recurring
        }, status=status.HTTP_200_OK)