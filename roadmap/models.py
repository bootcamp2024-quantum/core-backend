from django.db import models


class Roadmap(models.Model):
    published = models.BooleanField(default=False)
    title = models.CharField(max_length=255, unique=True)
    tags = models.ManyToManyField("Tag", related_name="r_tags", related_query_name="r_tag", )

    def __str__(self):
        return self.title


class Vertex(models.Model):
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE)
    depends = models.ManyToManyField("self", symmetrical=False, blank=True)
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

    tags = models.ManyToManyField("Tag", related_name="ic_tags", related_query_name="ic_tag")


class MetaDomain(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class LocalDomain(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class KnowledgeType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class EntryLevel(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
