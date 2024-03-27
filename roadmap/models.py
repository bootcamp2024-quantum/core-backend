from django.db import models


class Roadmap(models.Model):
    published = models.BooleanField(default=False)
    title = models.CharField(max_length=255, unique=True)
    tags = models.ManyToManyField("Tag", related_name="tags", related_query_name="tag", )


class Vertex(models.Model):
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE)
    depends = models.ManyToManyField("self", symmetrical=False)
    info_card = models.ForeignKey("InfoCard", on_delete=models.CASCADE)


class InfoCard(models.Model):
    # SET_NULL is selected for not dropping entire InfoCard instance
    # in case instance behind any of the next 4 references being dropped
    meta_domain = models.ForeignKey("MetaDomain", null=True, on_delete=models.SET_NULL)
    local_domain = models.ForeignKey("LocalDomain", null=True, on_delete=models.SET_NULL)
    knowledge_type = models.ForeignKey("KnowledgeType", null=True, on_delete=models.SET_NULL)
    entry_level = models.ForeignKey("EntryLevel", null=True, on_delete=models.SET_NULL)

    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    links = models.TextField(blank=True)

    tags = models.ManyToManyField("Tag", related_name="tags", related_query_name="tag")


class MetaDomain(models.Model):
    name = models.CharField(max_length=255, unique=True)


class LocalDomain(models.Model):
    name = models.CharField(max_length=255, unique=True)


class KnowledgeType(models.Model):
    name = models.CharField(max_length=255, unique=True)


class EntryLevel(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
