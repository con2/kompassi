# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Message'
        db.create_table(u'mailings_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Event'])),
            ('app_label', self.gf('django.db.models.fields.CharField')(max_length=63)),
            ('recipient_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'])),
            ('subject_template', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('body_template', self.gf('django.db.models.fields.TextField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('sent_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('expired_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'mailings', ['Message'])

        # Adding model 'PersonMessageSubject'
        db.create_table(u'mailings_personmessagesubject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('digest', self.gf('django.db.models.fields.CharField')(max_length=63, db_index=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'mailings', ['PersonMessageSubject'])

        # Adding model 'PersonMessageBody'
        db.create_table(u'mailings_personmessagebody', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('digest', self.gf('django.db.models.fields.CharField')(max_length=63, db_index=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'mailings', ['PersonMessageBody'])

        # Adding model 'PersonMessage'
        db.create_table(u'mailings_personmessage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mailings.Message'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Person'])),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mailings.PersonMessageSubject'])),
            ('body', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mailings.PersonMessageBody'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'mailings', ['PersonMessage'])


    def backwards(self, orm):
        # Deleting model 'Message'
        db.delete_table(u'mailings_message')

        # Deleting model 'PersonMessageSubject'
        db.delete_table(u'mailings_personmessagesubject')

        # Deleting model 'PersonMessageBody'
        db.delete_table(u'mailings_personmessagebody')

        # Deleting model 'PersonMessage'
        db.delete_table(u'mailings_personmessage')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.event': {
            'Meta': {'object_name': 'Event'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'homepage_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'name_genitive': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'name_illative': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'name_inessive': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'organization_name': ('django.db.models.fields.CharField', [], {'max_length': '63', 'blank': 'True'}),
            'organization_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '63'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Venue']"})
        },
        u'core.person': {
            'Meta': {'ordering': "['surname']", 'object_name': 'Person'},
            'anonymous': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '1023'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nick': ('django.db.models.fields.CharField', [], {'max_length': '1023', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '1023'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'core.venue': {
            'Meta': {'object_name': 'Venue'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'name_inessive': ('django.db.models.fields.CharField', [], {'max_length': '63'})
        },
        u'mailings.message': {
            'Meta': {'object_name': 'Message'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'body_template': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Event']"}),
            'expired_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipient_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']"}),
            'sent_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'subject_template': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'mailings.personmessage': {
            'Meta': {'object_name': 'PersonMessage'},
            'body': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mailings.PersonMessageBody']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mailings.Message']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Person']"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mailings.PersonMessageSubject']"})
        },
        u'mailings.personmessagebody': {
            'Meta': {'object_name': 'PersonMessageBody'},
            'digest': ('django.db.models.fields.CharField', [], {'max_length': '63', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'mailings.personmessagesubject': {
            'Meta': {'object_name': 'PersonMessageSubject'},
            'digest': ('django.db.models.fields.CharField', [], {'max_length': '63', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['mailings']