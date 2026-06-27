from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from .serializers import AccountSerializer
from .models import Account




class ListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        account = Account.objects.select_related("user", "currency").filter(user = request.user)
        serializer = AccountSerializer(account, many = True)
        
        return Response({
            "message": "Hisobingiz",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = AccountSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        
        return Response({
            "message": "Hisob muvaffaqiyatli yaratildi.",
            "data": serializer.data,
        }, status=status.HTTP_201_CREATED)
        


class AccountDetail(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        try:
            account = Account.objects.select_related("user", "currency").get(pk=pk, user = request.user)
        except Account.DoesNotExist:
            return Response({"error": "Hisob topilmadi."}, status=status.HTTP_404_NOT_FOUND)
    
        serializer = AccountSerializer(account)
        
        return Response({
            'message': f"Mana bu {pk} idga tegishli, Hisob raqam.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


    def patch(self, request, pk):
        try:
            account = Account.objects.select_related("user", "currency").get(pk=pk, user = request.user)
        except Account.DoesNotExist:
            return Response({"error": "Hisob topilmadi."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AccountSerializer(instance = account, data = request.data, partial = True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            "message": "Hisobingiz yangilandi",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


    def delete(self, request, pk):
        try:
            account = Account.objects.select_related("user", "currency").get(pk=pk, user = request.user)
        except Account.DoesNotExist:
            return Response({"error": "Hisob topilmadi."}, status=status.HTTP_404_NOT_FOUND)
        
        account.delete()
        return Response({"message": "Account o'chirildi."}, status=status.HTTP_200_OK)





















