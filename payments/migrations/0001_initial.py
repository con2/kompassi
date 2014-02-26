# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Payment'
        db.create_table(u'payments_payment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('test', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('VERSION', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('STAMP', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('REFERENCE', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('PAYMENT', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('STATUS', self.gf('django.db.models.fields.IntegerField')()),
            ('ALGORITHM', self.gf('django.db.models.fields.IntegerField')()),
            ('MAC', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'payments', ['Payment'])


    def backwards(self, orm):
        # Deleting model 'Payment'
        db.delete_table(u'payments_payment')


    models = {
        u'payments.payment': {
            'ALGORITHM': ('django.db.models.fields.IntegerField', [], {}),
            'MAC': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'Meta': {'object_name': 'Payment'},
            'PAYMENT': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'REFERENCE': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'STAMP': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'STATUS': ('django.db.models.fields.IntegerField', [], {}),
            'VERSION': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'test': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['payments']