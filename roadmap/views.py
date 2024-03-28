from rest_framework import generics, pagination

from roadmap.models import Roadmap
from roadmap.serializers import RoadmapSerializer


class RoadmapSearchPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class RoadmapSearchAPIView(generics.ListAPIView):
    serializer_class = RoadmapSerializer
    pagination_class = RoadmapSearchPagination

    def get_queryset(self):
        search_query = self.request.GET.get('search')
        meta_domain = self.request.GET.get('meta_domain')
        local_domain = self.request.GET.get('local_domain')
        entry_level = self.request.GET.get('entry_level')
        ordering = self.request.GET.get('ordering')

        queryset = Roadmap.objects.filter(published=True)

        # Apply filters based on query parameters
        if entry_level:
            queryset = queryset.filter(vertex__info_card__entry_level__name=entry_level)
        if meta_domain:
            queryset = queryset.filter(vertex__info_card__meta_domain__name=meta_domain)
        if local_domain:
            queryset = queryset.filter(vertex__info_card__local_domain__name=local_domain)

        # Apply search filter
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        # Apply ordering
        if ordering == 'asc':
            queryset = queryset.order_by('title')
        else:
            queryset = queryset.order_by('-title')

        return queryset
