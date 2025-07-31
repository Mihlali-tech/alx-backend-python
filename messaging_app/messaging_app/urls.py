from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),  # 👈 Must contain "api/"
    path('api-auth/', include('rest_framework.urls')),  # optional for login/logout UI
]
