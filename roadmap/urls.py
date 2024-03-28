from django.urls import path
from roadmap.views import RoadmapSearchAPIView

app_name = "roadmap"

urlpatterns = [
    path('search/', RoadmapSearchAPIView.as_view(), name='roadmap-search'),
]
