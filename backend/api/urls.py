from django.urls import include, path
# from .views import recipe_list
from .views import cat_list

urlpatterns = [ 
    path('recipes/', cat_list),
    # path('api/v1/', include(router.urls)),
    # path('api/v1/api-token-auth/', views.obtain_auth_token), 
] 
