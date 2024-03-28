from rest_framework import serializers

from roadmap.models import LocalDomain, MetaDomain


class MetaDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaDomain
        fields = ["id", "name"]


class LocalDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalDomain
        fields = ["id", "name"]
