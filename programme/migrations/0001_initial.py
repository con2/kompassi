# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProgrammeEventMeta'
        db.create_table(u'programme_programmeeventmeta', (
            ('event', self.gf('django.db.models.fields.related.OneToOneField')(related_name='programmeeventmeta', unique=True, primary_key=True, to=orm['core.Event'])),
            ('admin_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'])),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'programme', ['ProgrammeEventMeta'])

        # Adding model 'Category'
        db.create_table(u'programme_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Event'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1023)),
            ('style', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'programme', ['Category'])

        # Adding model 'Room'
        db.create_table(u'programme_room', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Venue'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1023)),
            ('order', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'programme', ['Room'])

        # Adding model 'Role'
        db.create_table(u'programme_role', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1023)),
            ('require_contact_info', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'programme', ['Role'])

        # Adding model 'Tag'
        db.create_table(u'programme_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('style', self.gf('django.db.models.fields.CharField')(default='label-default', max_length=15)),
        ))
        db.send_create_signal(u'programme', ['Tag'])

        # Adding model 'Programme'
        db.create_table(u'programme_programme', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['programme.Category'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1023)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('length', self.gf('django.db.models.fields.IntegerField')()),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['programme.Room'])),
        ))
        db.send_create_signal(u'programme', ['Programme'])

        # Adding M2M table for field tags on 'Programme'
        m2m_table_name = db.shorten_name(u'programme_programme_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('programme', models.ForeignKey(orm[u'programme.programme'], null=False)),
            ('tag', models.ForeignKey(orm[u'programme.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['programme_id', 'tag_id'])

        # Adding model 'ProgrammeRole'
        db.create_table(u'programme_programmerole', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Person'])),
            ('programme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['programme.Programme'])),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['programme.Role'])),
        ))
        db.send_create_signal(u'programme', ['ProgrammeRole'])

        # Adding model 'View'
        db.create_table(u'programme_view', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Event'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'programme', ['View'])

        # Adding M2M table for field rooms on 'View'
        m2m_table_name = db.shorten_name(u'programme_view_rooms')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('view', models.ForeignKey(orm[u'programme.view'], null=False)),
            ('room', models.ForeignKey(orm[u'programme.room'], null=False))
        ))
        db.create_unique(m2m_table_name, ['view_id', 'room_id'])


    def backwards(self, orm):
        # Deleting model 'ProgrammeEventMeta'
        db.delete_table(u'programme_programmeeventmeta')

        # Deleting model 'Category'
        db.delete_table(u'programme_category')

        # Deleting model 'Room'
        db.delete_table(u'programme_room')

        # Deleting model 'Role'
        db.delete_table(u'programme_role')

        # Deleting model 'Tag'
        db.delete_table(u'programme_tag')

        # Deleting model 'Programme'
        db.delete_table(u'programme_programme')

        # Removing M2M table for field tags on 'Programme'
        db.delete_table(db.shorten_name(u'programme_programme_tags'))

        # Deleting model 'ProgrammeRole'
        db.delete_table(u'programme_programmerole')

        # Deleting model 'View'
        db.delete_table(u'programme_view')

        # Removing M2M table for field rooms on 'View'
        db.delete_table(db.shorten_name(u'programme_view_rooms'))


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
        u'programme.category': {
            'Meta': {'ordering': "['title']", 'object_name': 'Category'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'style': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1023'})
        },
        u'programme.programme': {
            'Meta': {'ordering': "['start_time', 'room']", 'object_name': 'Programme'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['programme.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'organizers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Person']", 'through': u"orm['programme.ProgrammeRole']", 'symmetrical': 'False'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['programme.Room']"}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['programme.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1023'})
        },
        u'programme.programmeeventmeta': {
            'Meta': {'object_name': 'ProgrammeEventMeta'},
            'admin_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']"}),
            'event': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'programmeeventmeta'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['core.Event']"}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'programme.programmerole': {
            'Meta': {'object_name': 'ProgrammeRole'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Person']"}),
            'programme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['programme.Programme']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['programme.Role']"})
        },
        u'programme.role': {
            'Meta': {'ordering': "['title']", 'object_name': 'Role'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'require_contact_info': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1023'})
        },
        u'programme.room': {
            'Meta': {'ordering': "['venue', 'order']", 'object_name': 'Room'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1023'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Venue']"})
        },
        u'programme.tag': {
            'Meta': {'ordering': "['order']", 'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'style': ('django.db.models.fields.CharField', [], {'default': "'label-default'", 'max_length': '15'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        u'programme.view': {
            'Meta': {'ordering': "['order']", 'object_name': 'View'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'rooms': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['programme.Room']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['programme']