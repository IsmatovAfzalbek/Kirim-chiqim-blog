import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser


from .models import Currency, ExchangeRate
from .serializers import CurrencySerializer, ExchangeRateSerializer




class CurrencyListCreateView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        currencies = Currency.objects.all()
        serializer = CurrencySerializer(currencies, many=True)
        
        return Response({
            "message": serializer.data
            }, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = CurrencySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            "message": serializer.data
            }, status=status.HTTP_201_CREATED)



class CurrencyDetailView(APIView):
    permission_classes = [IsAuthenticated]


    def get_object(self, pk):
        try:
            return Currency.objects.get(pk=pk)
        except Currency.DoesNotExist:
            return None
        
    
    def get(self, request, pk):
        currency = self.get_object(pk)
        if currency is None:
            return Response({
                "error": "Valyuta topilmadi."
            }, status=status.HTTP_404_NOT_FOUND)
            
        serializer = CurrencySerializer(currency)
        return Response({
            "messages": serializer.data
            }, status=status.HTTP_200_OK)
            

    def patch(self, request, pk):
        currency = self.get_object(pk)
        if not currency:
            return Response({"error": "Valyuta topilmadi."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CurrencySerializer(currency, partial = True, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            "message": "Valyuta muvaffaqiyatli yangilandi.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        
        
    def delete(self, request, pk):
        currency = self.get_object(pk)
        if not currency:
            return Response({"error": "Valyuta topilmadi."}, status=status.HTTP_404_NOT_FOUND)
            
        currency.delete()
        return Response({"message": "Valyuta o'chirildi."}, status=status.HTTP_200_OK)

        
        
class FetchRateView(APIView):
    permission_classes = [IsAdminUser]


    def post(self, request):
        code = request.data.get("code")
        date = request.data.get("date")
        
        
        if not code or not date:
            return Response({"error": "Code va data majburiy."}, status=status.HTTP_400_BAD_REQUEST)   
        
        try:
            currency = Currency.objects.get(code=code.upper())
        except Currency.DoesNotExist:
            return Response({
                "error": "Bunday valyuta topilmadi."
                }, status=status.HTTP_404_NOT_FOUND)

        url = f"https://cbu.uz/uz/arkhiv-kursov-valyut/json/{code.upper()}/{date}/"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            rate_uzs = data[0]["Rate"]
        except requests.RequestException:
            return Response({"error": "CBU API dan kurs olishda xatolik."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        exchange_rate, created = ExchangeRate.objects.get_or_create(
            currency=currency,
            date=date,
            defaults={"rate_uzs": rate_uzs}
        )

        serializer = ExchangeRateSerializer(exchange_rate)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
