from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.serializers import RegisterSerializer, LogoutSerializer, CustomLoginSerializer, CustomRefreshSerializer
from accounts.models import User
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from accounts.filters import UserFilter
from rest_framework.filters import SearchFilter,OrderingFilter
from accounts.pagination import CustomUserPagination, CustomLimitOffsetPagination
# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = CustomLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = RefreshToken.for_user(serializer.validated_data['user'])
        access = refresh.access_token
        return Response({"refresh": str(refresh), "access": str(access)}, status=status.HTTP_200_OK)
    
    
    
class RefreshTokenView(APIView):
    def post(self, request):
        serializer = CustomRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
    


class UserListVIew(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter
    permission_classes = [AllowAny]


            

class UserSearchView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    filter_backends = [SearchFilter]  
    search_fields = ['username'] 
    permission_classes = [AllowAny]
    pagination_class = CustomLimitOffsetPagination 


class OrderingUserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['username', 'email']
    permission_classes = [AllowAny]
    pagination_class = CustomUserPagination

