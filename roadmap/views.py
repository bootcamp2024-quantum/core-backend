from rest_framework.response import Response
from rest_framework.views import APIView

from roadmap.models import LocalDomain, MetaDomain
from roadmap.serializers import LocalDomainSerializer, MetaDomainSerializer


class DomainListView(APIView):

    def get(self, request):
        meta_domains = MetaDomain.objects.all()
        local_domains = LocalDomain.objects.all()

        meta_domain_serializer = MetaDomainSerializer(meta_domains, many=True)
        local_domain_serializer = LocalDomainSerializer(local_domains, many=True)

        data = {
            "meta_domains": meta_domain_serializer.data,
            "local_domains": local_domain_serializer.data,
        }

        return Response(data)
