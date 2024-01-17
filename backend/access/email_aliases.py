from .utils import emailify


def firstname_surname(person):
    return emailify(f"{person.first_name} {person.surname}")


def nick(person):
    if person.nick:
        return emailify(person.nick)
    elif person.first_name:
        return emailify(person.first_name)
    else:
        return None
