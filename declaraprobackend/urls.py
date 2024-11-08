from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt import views as jwt_views 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('api.urls')),  # As outras rotas da sua aplicação
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
