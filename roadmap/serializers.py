from rest_framework import serializers
from roadmap import models


class RoadmapSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = models.Roadmap
        fields = ["pk", "title", "tags"]

    @staticmethod
    def get_tags(instance):
        return [tag.name for tag in instance.tags.all()]
