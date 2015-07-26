from django.contrib import admin

from models import SMSMessage, Hotword, VoteCategories, Vote


class SMSRecipientGroupAdmin(admin.ModelAdmin):
    list_display = ('app_label', 'event', 'verbose_name')
    list_filter = ('app_label', 'event')


class HotwordAdmin(admin.ModelAdmin):
    model = Hotword
    fields = ('hotword', 'slug', 'valid_from', 'valid_to', 'assigned_event')
    list_display = ('hotword', 'slug', 'valid_from', 'valid_to', 'assigned_event')
    list_filter = ('valid_from', 'valid_to', 'assigned_event')


class VoteCategoriesAdmin(admin.ModelAdmin):
    model = VoteCategories
    fields = ('category', 'slug', 'mapped', 'value_min', 'value_max')
    list_display = ('category', 'slug', 'mapped', 'value_min', 'value_max')
    list_filter = ('mapped', 'value_min', 'value_max')
    #fields = ('category', 'slug', 'value_min', 'value_max')
    #list_display = ('category', 'slug', 'value_min', 'value_max')
    #list_filter = ('value_min', 'value_max')


class VoteAdmin(admin.ModelAdmin):
    model = Vote
    fields = ('hotword', 'category', 'vote', 'voter')
    list_display = ('hotword', 'category', 'vote', 'voter')
    readonly_fields = ('hotword', 'category', 'vote', 'voter')

    def has_add_permission(self, request):
        return False


admin.site.register(SMSMessage)
admin.site.register(Hotword, HotwordAdmin)
admin.site.register(VoteCategories, VoteCategoriesAdmin)
admin.site.register(Vote, VoteAdmin)
#admin.site.register(SMSRecipientGroup, SMSRecipientGroupAdmin)
