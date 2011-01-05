from django.contrib import admin

from tmapi.models import Association, Name, Occurrence, Role, \
    SubjectIdentifier, SubjectLocator, Topic, TopicMap, Variant


class AssociationAdmin (admin.ModelAdmin):
    pass


class NameAdmin (admin.ModelAdmin):
    pass


class OccurrenceAdmin (admin.ModelAdmin):
    pass


class RoleAdmin (admin.ModelAdmin):
    pass


class SubjectIdentifierAdmin (admin.ModelAdmin):
    pass


class SubjectLocatorAdmin (admin.ModelAdmin):
    pass


class TopicAdmin (admin.ModelAdmin):
    pass


class TopicMapAdmin (admin.ModelAdmin):
    pass


class VariantAdmin (admin.ModelAdmin):
    pass


admin.site.register(Association, AssociationAdmin)
admin.site.register(Occurrence, OccurrenceAdmin)
admin.site.register(Name, NameAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(SubjectIdentifier, SubjectIdentifierAdmin)
admin.site.register(SubjectLocator, SubjectLocatorAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(TopicMap, TopicMapAdmin)
admin.site.register(Variant, VariantAdmin)
