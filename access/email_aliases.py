# encoding: utf-8

from .utils import emailify


def firstname_surname(person):
    return emailify(u'{person.first_name} {person.surname}'.format(person=person))

def nick(person):
    return emailify(person.nick)