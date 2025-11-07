from django.urls import path,include
from .views import (
    RegisterView, LoginView, RefreshTokenView, LogoutView,  UserSearchView, 
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('search/', UserSearchView.as_view(),name='search'),
    path('__debug__/', include('debug_toolbar.urls')),
   
]
