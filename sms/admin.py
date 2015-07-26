# encoding: utf-8

from django.contrib import admin

from models import SMSMessageOut, SMSMessageIn, SMSEvent, Hotword, VoteCategories, Vote


def get_event(obj):
    return obj.smsevent.event
get_event.short_description = u"Tapahtuma"

def get_sender(obj):
    return obj.message.sender
get_sender.short_description = u"Lähettäjä"

def get_message(obj):
    return obj.message.message
get_message.short_description = u"Viesti"

def get_send_time(obj):
    return obj.message.receive_timestamp
get_send_time.short_description = u"Vastaanotettu"

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


class VoteAdmin(admin.ModelAdmin):
    model = Vote
    fields = ('hotword', 'category', 'vote', 'voter')
    list_display = ('hotword', 'category', 'vote', 'voter')
    readonly_fields = ('hotword', 'category', 'vote', 'voter')

    def has_add_permission(self, request):
        return False


class SMSEventAdmin(admin.ModelAdmin):
    model = SMSEvent
    fields = ('event', 'sms_enabled', 'current', 'used_credit')
    list_display = ('event', 'sms_enabled', 'current', 'used_credit')
    readonly_fields = ('used_credit', )


class SMSMessageInAdmin(admin.ModelAdmin):
    model = SMSMessageIn
    fields = (get_event, get_sender, get_send_time, get_message)
    list_display = (get_event, get_sender, get_send_time, get_message)


admin.site.register(SMSMessageOut)
admin.site.register(SMSMessageIn, SMSMessageInAdmin)
admin.site.register(SMSEvent, SMSEventAdmin)
admin.site.register(Hotword, HotwordAdmin)
admin.site.register(VoteCategories, VoteCategoriesAdmin)
admin.site.register(Vote, VoteAdmin)
#admin.site.register(SMSRecipientGroup, SMSRecipientGroupAdmin)
