"""
URL configuration for core_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from user.views import CustomTokenObtainPairView, CustomTokenRefreshView

from .docs_drf_yasg import urlpatterns as doc_urls

auth_patterns = [
    path("token/", CustomTokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token-refresh")
]

api_patterns = [
    path('', include(auth_patterns)),
    path("users/", include("user.urls", namespace="user"))
]
api_patterns.extend(doc_urls)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_patterns))
]

admin.site.site_header = 'Career Skill | Atlas Administration'
admin.site.index_title = 'Career Skill | Atlas administration'
admin.site.site_title = 'Career Skill | Atlas admin'
