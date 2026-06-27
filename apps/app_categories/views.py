from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Category
from .serializers import CategorySerializer





class CategoryListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.select_related("user").filter(user=request.user)
        serializer = CategorySerializer(categories, many=True)
        
        return Response({
            "data": serializer.data
        }, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        
        return Response({
            "message": "Kategoriya muvaffaqiyatli yaratildi.",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)



class CategoryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            category = Category.objects.select_related("user").get(pk=pk, user = request.user)
        except Category.DoesNotExist:
            return Response({"error": "Kategoriya topilmadi."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategorySerializer(category)
        return Response({
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        
        
    def patch(self, request, pk):
        try:
            category = Category.objects.select_related('user').get(pk=pk, user=request.user)
        except Category.DoesNotExist:
            return Response({"error": "Kategoriya topilmadi."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategorySerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            "message": "Kategoriya yangilandi.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        
        
    def delete(self, request, pk):
        try:
            category = Category.objects.select_related('user').get(pk=pk, user=request.user)
        except Category.DoesNotExist:
            return Response({"error": "Kategoriya topilmadi."}, status=status.HTTP_404_NOT_FOUND)
        
        category.delete()
        return Response({"message": "Kategoriya o'chirildi."}, status=status.HTTP_200_OK)














