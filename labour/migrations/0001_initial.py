# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LabourEventMeta'
        db.create_table(u'labour_laboureventmeta', (
            ('event', self.gf('django.db.models.fields.related.OneToOneField')(related_name='laboureventmeta', unique=True, primary_key=True, to=orm['core.Event'])),
            ('admin_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'])),
            ('signup_extra_content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('registration_opens', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('registration_closes', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('work_begins', self.gf('django.db.models.fields.DateTimeField')()),
            ('work_ends', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'labour', ['LabourEventMeta'])

        # Adding model 'Qualification'
        db.create_table(u'labour_qualification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=63)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=63)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('qualification_extra_content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
        ))
        db.send_create_signal(u'labour', ['Qualification'])

        # Adding model 'PersonQualification'
        db.create_table(u'labour_personqualification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Person'])),
            ('qualification', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['labour.Qualification'])),
        ))
        db.send_create_signal(u'labour', ['PersonQualification'])

        # Adding model 'JobCategory'
        db.create_table(u'labour_jobcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Event'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=63)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'labour', ['JobCategory'])

        # Adding M2M table for field required_qualifications on 'JobCategory'
        m2m_table_name = db.shorten_name(u'labour_jobcategory_required_qualifications')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('jobcategory', models.ForeignKey(orm[u'labour.jobcategory'], null=False)),
            ('qualification', models.ForeignKey(orm[u'labour.qualification'], null=False))
        ))
        db.create_unique(m2m_table_name, ['jobcategory_id', 'qualification_id'])

        # Adding model 'WorkPeriod'
        db.create_table(u'labour_workperiod', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Event'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=63, blank=True)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'labour', ['WorkPeriod'])

        # Adding model 'Job'
        db.create_table(u'labour_job', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['labour.JobCategory'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=63)),
        ))
        db.send_create_signal(u'labour', ['Job'])

        # Adding model 'JobRequirement'
        db.create_table(u'labour_jobrequirement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['labour.Job'])),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'labour', ['JobRequirement'])

        # Adding model 'Signup'
        db.create_table(u'labour_signup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Person'])),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Event'])),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('job_accepted', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='accepted_signup_set', null=True, to=orm['labour.JobCategory'])),
            ('is_rejected', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'labour', ['Signup'])

        # Adding M2M table for field job_categories on 'Signup'
        m2m_table_name = db.shorten_name(u'labour_signup_job_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('signup', models.ForeignKey(orm[u'labour.signup'], null=False)),
            ('jobcategory', models.ForeignKey(orm[u'labour.jobcategory'], null=False))
        ))
        db.create_unique(m2m_table_name, ['signup_id', 'jobcategory_id'])

        # Adding M2M table for field work_periods on 'Signup'
        m2m_table_name = db.shorten_name(u'labour_signup_work_periods')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('signup', models.ForeignKey(orm[u'labour.signup'], null=False)),
            ('workperiod', models.ForeignKey(orm[u'labour.workperiod'], null=False))
        ))
        db.create_unique(m2m_table_name, ['signup_id', 'workperiod_id'])

        # Adding model 'EmptySignupExtra'
        db.create_table(u'labour_emptysignupextra', (
            ('signup', self.gf('django.db.models.fields.related.OneToOneField')(related_name='+', unique=True, primary_key=True, to=orm['labour.Signup'])),
        ))
        db.send_create_signal(u'labour', ['EmptySignupExtra'])


    def backwards(self, orm):
        # Deleting model 'LabourEventMeta'
        db.delete_table(u'labour_laboureventmeta')

        # Deleting model 'Qualification'
        db.delete_table(u'labour_qualification')

        # Deleting model 'PersonQualification'
        db.delete_table(u'labour_personqualification')

        # Deleting model 'JobCategory'
        db.delete_table(u'labour_jobcategory')

        # Removing M2M table for field required_qualifications on 'JobCategory'
        db.delete_table(db.shorten_name(u'labour_jobcategory_required_qualifications'))

        # Deleting model 'WorkPeriod'
        db.delete_table(u'labour_workperiod')

        # Deleting model 'Job'
        db.delete_table(u'labour_job')

        # Deleting model 'JobRequirement'
        db.delete_table(u'labour_jobrequirement')

        # Deleting model 'Signup'
        db.delete_table(u'labour_signup')

        # Removing M2M table for field job_categories on 'Signup'
        db.delete_table(db.shorten_name(u'labour_signup_job_categories'))

        # Removing M2M table for field work_periods on 'Signup'
        db.delete_table(db.shorten_name(u'labour_signup_work_periods'))

        # Deleting model 'EmptySignupExtra'
        db.delete_table(u'labour_emptysignupextra')


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
            'admin_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']"}),
            'event': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'laboureventmeta'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['core.Event']"}),
            'registration_closes': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'registration_opens': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'signup_extra_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'work_begins': ('django.db.models.fields.DateTimeField', [], {}),
            'work_ends': ('django.db.models.fields.DateTimeField', [], {})
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