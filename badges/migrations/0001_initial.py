# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BadgesEventMeta'
        db.create_table(u'badges_badgeseventmeta', (
            ('event', self.gf('django.db.models.fields.related.OneToOneField')(related_name='badgeseventmeta', unique=True, primary_key=True, to=orm['core.Event'])),
            ('admin_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'])),
            ('badge_factory_code', self.gf('django.db.models.fields.CharField')(default='badges.utils:default_badge_factory', max_length='255')),
        ))
        db.send_create_signal(u'badges', ['BadgesEventMeta'])

        # Adding model 'Template'
        db.create_table(u'badges_template', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Event'])),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=63)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=63)),
        ))
        db.send_create_signal(u'badges', ['Template'])

        # Adding unique constraint on 'Template', fields ['event', 'slug']
        db.create_unique(u'badges_template', ['event_id', 'slug'])

        # Adding model 'Batch'
        db.create_table(u'badges_batch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['badges.Template'])),
            ('printed_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'badges', ['Batch'])

        # Adding model 'Badge'
        db.create_table(u'badges_badge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Person'], null=True, blank=True)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['badges.Template'])),
            ('time_printed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('time_revoked', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('job_title', self.gf('django.db.models.fields.CharField')(default=u'', max_length=63, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'badges', ['Badge'])


    def backwards(self, orm):
        # Removing unique constraint on 'Template', fields ['event', 'slug']
        db.delete_unique(u'badges_template', ['event_id', 'slug'])

        # Deleting model 'BadgesEventMeta'
        db.delete_table(u'badges_badgeseventmeta')

        # Deleting model 'Template'
        db.delete_table(u'badges_template')

        # Deleting model 'Batch'
        db.delete_table(u'badges_batch')

        # Deleting model 'Badge'
        db.delete_table(u'badges_badge')


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
        u'badges.badge': {
            'Meta': {'object_name': 'Badge'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_title': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '63', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Person']", 'null': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['badges.Template']"}),
            'time_printed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'time_revoked': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'badges.badgeseventmeta': {
            'Meta': {'object_name': 'BadgesEventMeta'},
            'admin_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']"}),
            'badge_factory_code': ('django.db.models.fields.CharField', [], {'default': "'badges.utils:default_badge_factory'", 'max_length': "'255'"}),
            'event': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'badgeseventmeta'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['core.Event']"})
        },
        u'badges.batch': {
            'Meta': {'object_name': 'Batch'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'printed_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['badges.Template']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'badges.template': {
            'Meta': {'unique_together': "[('event', 'slug')]", 'object_name': 'Template'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '63'})
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
            'headline': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '63', 'blank': 'True'}),
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
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'blank': 'True'}),
            'email_verified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '1023'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'may_send_info': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nick': ('django.db.models.fields.CharField', [], {'max_length': '1023', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'preferred_name_display_style': ('django.db.models.fields.CharField', [], {'max_length': '31', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '1023'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'core.venue': {
            'Meta': {'object_name': 'Venue'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'name_inessive': ('django.db.models.fields.CharField', [], {'max_length': '63'})
        }
    }

    complete_apps = ['badges']