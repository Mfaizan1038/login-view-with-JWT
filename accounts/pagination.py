from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

class CustomUserPagination(PageNumberPagination):
    page_size = 5                     
    max_page_size = 50 



class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5        
    max_limit = 50 