from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


from .models import CustomUser
from .serilaizers import RegisterSerializer, LoginSerializer, ProfileSerializer, ProfileUpdateSerializer



class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    
    def post(self, request):
        serializer = RegisterSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            "message": "Muvaffaqiyatli ro'yxatdan o'tdingiz!",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
        
        
class LoginView(APIView):
    permission_classes = [AllowAny]
    
    
    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)    
        
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        
        return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }, status=status.HTTP_200_OK)    
        
        

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
        
    
    def get(self, request):
        profile = ProfileSerializer(request.user)
        
        return Response({
            "message": "Profile",
            "data": profile.data,
        }, status=status.HTTP_200_OK)
        
        
    def patch(self, request):
        serializer = ProfileUpdateSerializer(request.user, data = request.data, partial = True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            "message": "Muvaffaqiyatli o'zgartirildi",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        
        
    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        
        return Response({
            "message": "Akkaunt deaktiv qilindi."
            }, status=status.HTTP_200_OK)
            
        
        
class NewToken(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh")
        
        try:
           refresh = RefreshToken(refresh_token)
           return Response({
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        except Exception:
            raise ValidationError({"error": "Token yaroqsiz yoki muddati tugagan."})   
        
                    

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
