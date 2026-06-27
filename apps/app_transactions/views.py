from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .filters import TransactionFilter


from .models import Transaction, RecurringTransaction
from .serializers import TransactionSerializer, RecurringTransactionSerializer





class TransactionListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    class TransactionListCreateView(APIView):
        permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.select_related(
            'user', 'account', 'category', 'currency'
        ).filter(user=request.user)

        filterset = TransactionFilter(request.GET, queryset=transactions)
        serializer = TransactionSerializer(filterset.qs, many=True)

        return Response({
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        

    def post(self, request):
        serializer = TransactionSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        
        return Response({
            "message": "Tranzaksiya muvaffaqiyatli yaratildi.",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)



class TransactionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            transaction = Transaction.objects.select_related(
                "user", "account", "category", "currency"
                ).get(pk=pk, user=request.user)

        except Transaction.DoesNotExist:
             return Response({"error": "Tranzaksiya topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TransactionSerializer(transaction)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
    
    def patch(self, request, pk):
        try:
            transaction = Transaction.objects.select_related(
                "user", "account", "category", "currency"
            ).get(pk=pk, user=request.user)
        except Transaction.DoesNotExist:
            return Response({"error": "Tranzaksiya topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TransactionSerializer(instance = transaction, data = request.data, partial = True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            "message": "Tranzaksiya yangilandi.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
            

    def delete(self, request, pk):
        try:
            transaction = Transaction.objects.select_related(
                "user", "account", "category", "currency"
            ).get(pk=pk, user=request.user)
            
        except Transaction.DoesNotExist:
            return Response({"error": "Tranzaksiya topilmadi."}, status=status.HTTP_404_NOT_FOUND)
        
        transaction.delete()
        return Response({"message": "Tranzaksiya o'chirildi."}, status=status.HTTP_200_OK)



class RecurringTransactionListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        transactions = RecurringTransaction.objects.select_related(
            "user", "account", "category", "currency"
        ).filter(user=request.user)
        serializer = RecurringTransactionSerializer(transactions, many=True)
        
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        
        
    def post(self, request):
        serializer = RecurringTransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        
        return Response({
            "message": "Takrorlanuvchi tranzaksiya yaratildi.",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)



class RecurringTransactionDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        try:
            transaction = RecurringTransaction.objects.select_related(
                'user', 'account', 'category', 'currency'
            ).get(pk=pk, user=request.user)
        except RecurringTransaction.DoesNotExist:
            return Response({"error": "Topilmadi."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = RecurringTransactionSerializer(transaction)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    

    def patch(self, request, pk):
        try:
            transaction = RecurringTransaction.objects.select_related(
                "user", "account", "category", "currency"
            ).get(user=request.user, pk=pk)
        except RecurringTransaction.DoesNotExist:
             return Response({"error": "Topilmadi."}, status=status.HTTP_404_NOT_FOUND)
         
        serializer = RecurringTransactionSerializer(transaction, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            "message": "Yangilandi.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


    def delete(self, request, pk):
        try:
            transaction = RecurringTransaction.objects.select_related(
                'user', 'account', 'category', 'currency'
            ).get(pk=pk, user=request.user)
        except RecurringTransaction.DoesNotExist:
            return Response({"error": "Topilmadi."}, status=status.HTTP_404_NOT_FOUND)
        
        transaction.delete()
        return Response({"message": "O'chirildi."}, status=status.HTTP_200_OK)












