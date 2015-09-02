# encoding: utf-8

from django.conf import settings
from django.dispatch import receiver
from django.utils import timezone

import regex
from nexmo.models import InboundMessage, message_received

from .models import (
    Hotword,
    InboundMessage,
    Nominee,
    SMSEventMeta,
    SMSMessageIn,
    Vote,
    VoteCategory,
)


# TODO Needs massive refactoring.
# Now this has two responsibilities intertwined:
# - determine which facility should handle the incoming message
# - implement the SMS voting system
# These should be split into two different facilities:
# 1. a generic inbound SMS handler that looks up a list of eg. (regex, handler) pairs
# 2. an SMS voting handler
@receiver(message_received)
def sms_received_handler(sender, **kwargs):
    messages = InboundMessage.objects.filter(nexmo_message_id=kwargs['nexmo_message_id'])
    message = messages[0]  # If nexmo has delivered same message multiple times.
    now = timezone.now()
    hotwords = Hotword.objects.filter(valid_from__lte=now, valid_to__gte=now)
    match = regex.match(r'(?P<hotword>[a-z]+) ((?P<category>[a-z]*)(?:\s?)(?P<vote>\d+))', message.message.lower())  # doesn't work with pythons re. Recursive patterns are not allowed.
    if match is not None:
        # Message with hotword
        for hotword in hotwords:
            found = False
            if hotword.slug == match.group('hotword'):
                found = hotword
                break
        if found is not False:
            # Valid hotword found, check category.
            if match.group('category') == '':
                # no category, checking if there should be
                try:
                    nominee = Nominee.objects.get(number=int(match.group('vote')), category__hotword=found)
                except Nominee.DoesNotExist:
                    # Ok,  there was none,  or vote value out of scope, vote rejected.
                    vote = "rejected"
                except Nominee.MultipleObjectsReturned:
                    try:
                        nominee = Nominee.objects.get(number=match.group('vote'), category__primary=True, category__hotword=found)
                    except Nominee.DoesNotExist:
                        vote = "rejected"
                    else:
                        try:
                            category = VoteCategory.objects.get(nominee=nominee,primary=True)
                            existing_vote = Vote.objects.get(message__sender=message.sender,category=category)
                        except Vote.DoesNotExist:
                            # No old vote
                            vote = Vote(category=category,vote=nominee,message=message)
                            vote.save()
                        else:
                            existing_vote.vote = nominee
                            existing_vote.message = message
                            existing_vote.category = category
                            existing_vote.save()
                else:
                    try:
                        category = nominee.category.all()[0]
                        existing_vote = Vote.objects.get(message__sender=message.sender,category=category)
                    except Vote.DoesNotExist:
                        # No old vote
                        vote = Vote(category=category,vote=nominee,message=message)
                        vote.save()
                    else:
                        existing_vote.vote = nominee
                        existing_vote.message = message
                        existing_vote.category = category
                        existing_vote.save()

            else:
                try:
                    nominee = Nominee.objects.get(number=match.group('vote'), category__slug=match.group('category'), category__hotword=found)
                except Nominee.DoesNotExist:
                    vote = "rejected"
                else:
                    try:
                        category = VoteCategory.objects.get(slug=match.group('category'))
                        existing_vote = Vote.objects.get(message__sender=message.sender,vote=nominee)
                    except Vote.DoesNotExist:
                        # No old vote
                        vote = Vote(category=category,vote=nominee,message=message)
                        vote.save()
                    else:
                        existing_vote.vote = nominee
                        existing_vote.message = message
                        existing_vote.category = category
                        existing_vote.save()
        else:
            # Voting message with non-valid hotword.
            # It is very unlikely to someone start their message with "I am 13" or something like it (word [word] digit)
            # But hadle it anyway as regular message
            try:
                event = SMSEventMeta.objects.get(current=True, sms_enabled=True)
            except SMSEventMeta.DoesNotExist:
                # Don't know to which event point the new message, ignored.
                pass
            else:
                new_message = SMSMessageIn(message=message, SMSEventMeta=event)
                new_message.save()
    else:
        #regular message with no hotword.
        try:
            event = SMSEventMeta.objects.get(current=True, sms_enabled=True)
        except SMSEventMeta.DoesNotExist:
            # Don't know to which event point the new message, ignored.
            pass
        else:
            new_message = SMSMessageIn(message=message, SMSEventMeta=event)
            new_message.save()
