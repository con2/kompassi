# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ExtraDomain'
        db.create_table(u'extra_domains_extradomain', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('domain_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=63)),
            ('root_urlconf', self.gf('django.db.models.fields.CharField')(max_length=63)),
        ))
        db.send_create_signal(u'extra_domains', ['ExtraDomain'])

        # Adding model 'ViewArg'
        db.create_table(u'extra_domains_viewarg', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('extra_domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['extra_domains.ExtraDomain'])),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=63)),
        ))
        db.send_create_signal(u'extra_domains', ['ViewArg'])

        # Adding model 'ViewKwarg'
        db.create_table(u'extra_domains_viewkwarg', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('extra_domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['extra_domains.ExtraDomain'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=63)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=63)),
        ))
        db.send_create_signal(u'extra_domains', ['ViewKwarg'])


    def backwards(self, orm):
        # Deleting model 'ExtraDomain'
        db.delete_table(u'extra_domains_extradomain')

        # Deleting model 'ViewArg'
        db.delete_table(u'extra_domains_viewarg')

        # Deleting model 'ViewKwarg'
        db.delete_table(u'extra_domains_viewkwarg')


    models = {
        u'extra_domains.extradomain': {
            'Meta': {'object_name': 'ExtraDomain'},
            'domain_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '63'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'root_urlconf': ('django.db.models.fields.CharField', [], {'max_length': '63'})
        },
        u'extra_domains.viewarg': {
            'Meta': {'object_name': 'ViewArg'},
            'extra_domain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['extra_domains.ExtraDomain']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '63'})
        },
        u'extra_domains.viewkwarg': {
            'Meta': {'object_name': 'ViewKwarg'},
            'extra_domain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['extra_domains.ExtraDomain']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '63'})
        }
    }

    complete_apps = ['extra_domains']