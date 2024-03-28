from django.contrib import admin

from roadmap import models


class RoadmapAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'published')


class InfoCardAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'knowledge_type', 'meta_domain', 'local_domain')


class VertexAdmin(admin.ModelAdmin):
    list_display = ('id', 'roadmap', 'info_card')


admin.site.register(models.Roadmap, RoadmapAdmin)
admin.site.register(models.InfoCard,InfoCardAdmin)
admin.site.register(models.Vertex,VertexAdmin)


class SmallModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


admin.site.register(models.MetaDomain, SmallModelAdmin)
admin.site.register(models.LocalDomain, SmallModelAdmin)
admin.site.register(models.KnowledgeType, SmallModelAdmin)
admin.site.register(models.EntryLevel, SmallModelAdmin)
admin.site.register(models.Tag, SmallModelAdmin)
