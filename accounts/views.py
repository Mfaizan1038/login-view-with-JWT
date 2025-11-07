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

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save() 
        return Response(
            {
                "message": "User registered",
                "user": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return Response({
            "access": str(access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)
    
    
    
    
class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = serializer.validated_data['refresh']
        refresh_token = RefreshToken(refresh)
        access_token = refresh_token.access_token

        return Response({
            "access_token": str(access_token)
        }, status=status.HTTP_200_OK)

    
    
      

class LogoutView(generics.CreateAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = serializer.validated_data['refresh']
        token= RefreshToken(refresh).blacklist()
        return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)

    
    



class UserSearchView(APIView):
    permission_classes = [AllowAny]
    filter_backend = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = UserFilter
    search_fields = ['username', 'email']
    ordering_fields = ['username', 'email']

    def get_quryset(self, request):
        queryset = User.objects.all()
        for backend in self.filter_backend:
            queryset = backend().filter_queryset(request, queryset, self)
        return queryset

    def get(self, request):
        queryset = self.get_quryset(request)
        paginator = CustomUserPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = RegisterSerializer(paginated_queryset, many=True)

        return Response(serializer.data)
