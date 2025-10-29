
from django.contrib import admin
from django.urls import path , include
try:
    from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
    _HAS_SPECTACULAR = True
except Exception:
    _HAS_SPECTACULAR = False

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app_Empresa.urls_E')),
    path('api/User/', include('app_User.urls')),
]

if _HAS_SPECTACULAR:
    urlpatterns += [
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]
