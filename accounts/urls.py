from django.urls import path,include
from .views import (
    RegisterView, LoginView, RefreshTokenView, LogoutView, UserListVIew, UserSearchView, OrderingUserListView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', UserListVIew.as_view(),),
    path('search/', UserSearchView.as_view(),),
    path('ordering/', OrderingUserListView.as_view(),),
    path('__debug__/', include('debug_toolbar.urls')),
   
]
