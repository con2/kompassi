# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Message'
        db.create_table(u'labour_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Event'])),
            ('recipient_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'])),
            ('subject_template', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('body_template', self.gf('django.db.models.fields.TextField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('sent_at', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('expired_at', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
        ))
        db.send_create_signal(u'labour', ['Message'])

        # Adding model 'PersonMessageBody'
        db.create_table(u'labour_personmessagebody', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('digest', self.gf('django.db.models.fields.CharField')(max_length=63, db_index=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'labour', ['PersonMessageBody'])

        # Adding model 'PersonMessageSubject'
        db.create_table(u'labour_personmessagesubject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('digest', self.gf('django.db.models.fields.CharField')(max_length=63, db_index=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'labour', ['PersonMessageSubject'])

        # Adding model 'PersonMessage'
        db.create_table(u'labour_personmessage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['labour.Message'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Person'])),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['labour.PersonMessageSubject'])),
            ('body', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['labour.PersonMessageBody'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'labour', ['PersonMessage'])

        # Adding field 'LabourEventMeta.monitor_email'
        db.add_column(u'labour_laboureventmeta', 'monitor_email',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'LabourEventMeta.accepted_group'
        db.add_column(u'labour_laboureventmeta', 'accepted_group',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['auth.Group']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Message'
        db.delete_table(u'labour_message')

        # Deleting model 'PersonMessageBody'
        db.delete_table(u'labour_personmessagebody')

        # Deleting model 'PersonMessageSubject'
        db.delete_table(u'labour_personmessagesubject')

        # Deleting model 'PersonMessage'
        db.delete_table(u'labour_personmessage')

        # Deleting field 'LabourEventMeta.monitor_email'
        db.delete_column(u'labour_laboureventmeta', 'monitor_email')

        # Deleting field 'LabourEventMeta.accepted_group'
        db.delete_column(u'labour_laboureventmeta', 'accepted_group_id')


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
        u'labour.emptysignupextra': {
            'Meta': {'object_name': 'EmptySignupExtra'},
            'signup': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['labour.Signup']"})
        },
        u'labour.job': {
            'Meta': {'object_name': 'Job'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['labour.JobCategory']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '63'})
        },
        u'labour.jobcategory': {
            'Meta': {'object_name': 'JobCategory'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'required_qualifications': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['labour.Qualification']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'labour.jobrequirement': {
            'Meta': {'object_name': 'JobRequirement'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['labour.Job']"}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'labour.laboureventmeta': {
            'Meta': {'object_name': 'LabourEventMeta'},
            'accepted_group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['auth.Group']"}),
            'admin_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']"}),
            'event': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'laboureventmeta'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['core.Event']"}),
            'monitor_email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'registration_closes': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'registration_opens': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'signup_extra_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'work_begins': ('django.db.models.fields.DateTimeField', [], {}),
            'work_ends': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'labour.message': {
            'Meta': {'object_name': 'Message'},
            'body_template': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Event']"}),
            'expired_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipient_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']"}),
            'sent_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'subject_template': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'labour.personmessage': {
            'Meta': {'object_name': 'PersonMessage'},
            'body': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['labour.PersonMessageBody']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['labour.Message']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Person']"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['labour.PersonMessageSubject']"})
        },
        u'labour.personmessagebody': {
            'Meta': {'object_name': 'PersonMessageBody'},
            'digest': ('django.db.models.fields.CharField', [], {'max_length': '63', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'labour.personmessagesubject': {
            'Meta': {'object_name': 'PersonMessageSubject'},
            'digest': ('django.db.models.fields.CharField', [], {'max_length': '63', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'labour.personqualification': {
            'Meta': {'object_name': 'PersonQualification'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Person']"}),
            'qualification': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['labour.Qualification']"})
        },
        u'labour.qualification': {
            'Meta': {'object_name': 'Qualification'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'qualification_extra_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '63'})
        },
        u'labour.signup': {
            'Meta': {'object_name': 'Signup'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_rejected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_accepted': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'accepted_signup_set'", 'null': 'True', 'to': u"orm['labour.JobCategory']"}),
            'job_categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'signup_set'", 'symmetrical': 'False', 'to': u"orm['labour.JobCategory']"}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Person']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'work_periods': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'signup_set'", 'symmetrical': 'False', 'to': u"orm['labour.WorkPeriod']"})
        },
        u'labour.workperiod': {
            'Meta': {'object_name': 'WorkPeriod'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '63', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['labour']