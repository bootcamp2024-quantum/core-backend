from django.urls import path

from roadmap.views import DomainListView

app_name = "roadmaps"

urlpatterns = [
    path("domains/", DomainListView.as_view(), name="domains-get-all"),
]
