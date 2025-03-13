from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Pos_Main_App.api.views import health_check  # ✅ Correct import path

urlpatterns = [
    path('admin/', admin.site.urls),  # Django Admin Panel

    # ✅ API routes
    path('api/', include('Pos_Main_App.api.urls')),

    # ✅ Health Check Route
    path('api/health/', health_check, name='health_check'),

    # ✅ Only keep 'Home/' if it's required
    path('Home/', include('Pos_Main_App.api.urls')),  
]

# Serve media files in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
