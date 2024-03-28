from rest_framework import serializers
from roadmap import models


# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Tag
#         fields = ["name"]
#
#
# class RoadmapSerializer(serializers.ModelSerializer):
#     tags = TagSerializer(many=True)
#
#     class Meta:
#         model = models.Roadmap
#         fields = ["pk", "title", "tags"]
class RoadmapSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = models.Roadmap
        fields = ["pk", "title", "tags"]

    @staticmethod
    def get_tags(instance):
        return [tag.name for tag in instance.tags.all()]