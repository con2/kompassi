# encoding: utf-8

from __future__ import unicode_literals

import graphene

from core.schema import Query as CoreQuery


class Query(CoreQuery):
    pass


schema = graphene.Schema(name='Kompassi')
schema.query = Query
