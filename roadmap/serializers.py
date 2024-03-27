from rest_framework import serializers
from . import models


class MetaDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MetaDomain
        fields = ["name"]


class LocalDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LocalDomain
        fields = ["name"]


class KnowledgeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KnowledgeType
        fields = ["name"]


class EntryLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EntryLevel
        fields = ["name"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ["name"]


class InfoCardSerializer(serializers.ModelSerializer):
    meta_domain = MetaDomainSerializer()
    local_domain = LocalDomainSerializer()
    knowledge_type = KnowledgeTypeSerializer()
    entry_level = EntryLevelSerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = models.InfoCard
        fields = ["meta_domain", "local_domain",
                  "knowledge_type", "entry_level",
                  "title", "description",
                  "links", "tags"]


class RoadmapSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = models.Roadmap
        fields = ["published", "title", "tags"]


class VertexSerializer(serializers.ModelSerializer):
    roadmap = RoadmapSerializer()
    depends = serializers.PrimaryKeyRelatedField(many=True)
    info_card = InfoCardSerializer()

    class Meta:
        model = models.Vertex
        fields = ["roadmap", "depends", "info_card"]
