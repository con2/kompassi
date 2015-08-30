# encoding: utf-8

from django.contrib import admin

from models import SMSMessageOut, SMSMessageIn, SMSEventMeta, Hotword, VoteCategory, Vote, Nominee


def get_event(obj):
    return obj.SMSEventMeta.event
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

def format_price(obj):
    return u"%d,%02d €" % divmod(obj.used_credit, 100)
format_price.short_description = u"Käytetty krediitti"

class SMSRecipientGroupAdmin(admin.ModelAdmin):
    list_display = ('app_label', 'event', 'verbose_name')
    list_filter = ('app_label', 'event')


class HotwordAdmin(admin.ModelAdmin):
    model = Hotword
    fields = ('hotword', 'slug', 'valid_from', 'valid_to', 'assigned_event')
    list_display = ('hotword', 'slug', 'valid_from', 'valid_to', 'assigned_event')
    list_filter = ('valid_from', 'valid_to', 'assigned_event')


class VoteCategoryAdmin(admin.ModelAdmin):
    model = VoteCategory
    fields = ('category', 'slug', 'hotword','primary')
    list_display = ('category', 'slug', 'hotword', 'primary')
    list_filter = ('hotword',)


class VoteAdmin(admin.ModelAdmin):
    model = Vote
    list_display = ('category', 'vote', 'message', get_send_time)
    readonly_fields = ('category', 'vote', 'message', get_send_time)

    def has_add_permission(self, request):
        return False


class SMSEventMetaAdmin(admin.ModelAdmin):
    model = SMSEventMeta
    list_display = ('event', 'sms_enabled', 'current', format_price)
    readonly_fields = ('used_credit', )


class SMSMessageInAdmin(admin.ModelAdmin):
    model = SMSMessageIn
    list_display = (get_event, get_sender, get_send_time, get_message)


class CategoryAdmin(admin.StackedInline):
    model = Nominee.category.through


class NomineeAdmin(admin.ModelAdmin):
    model = Nominee
    list_display = ('name', 'number')
    inlines = [CategoryAdmin, ]


class SMSMessageOutAdmin(admin.ModelAdmin):
    model = SMSMessageOut
    list_display = ('to', 'message', 'event')


admin.site.register(SMSMessageOut, SMSMessageOutAdmin)
admin.site.register(SMSMessageIn, SMSMessageInAdmin)
admin.site.register(SMSEventMeta, SMSEventMetaAdmin)
admin.site.register(Hotword, HotwordAdmin)
admin.site.register(VoteCategory, VoteCategoryAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Nominee, NomineeAdmin)
