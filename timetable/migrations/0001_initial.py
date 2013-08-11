# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'timetable_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1023)),
            ('style', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'timetable', ['Category'])

        # Adding model 'Room'
        db.create_table(u'timetable_room', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1023)),
            ('order', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'timetable', ['Room'])

        # Adding model 'Person'
        db.create_table(u'timetable_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=1023)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=1023)),
            ('nick', self.gf('django.db.models.fields.CharField')(max_length=1023, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('anonymous', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'timetable', ['Person'])

        # Adding model 'Role'
        db.create_table(u'timetable_role', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1023)),
            ('require_contact_info', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'timetable', ['Role'])

        # Adding model 'Programme'
        db.create_table(u'timetable_programme', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1023)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('length', self.gf('django.db.models.fields.IntegerField')()),
            ('hilight', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timetable.Category'])),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timetable.Room'])),
        ))
        db.send_create_signal(u'timetable', ['Programme'])

        # Adding model 'ProgrammeRole'
        db.create_table(u'timetable_programmerole', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timetable.Person'])),
            ('programme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timetable.Programme'])),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timetable.Role'])),
        ))
        db.send_create_signal(u'timetable', ['ProgrammeRole'])

        # Adding model 'View'
        db.create_table(u'timetable_view', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'timetable', ['View'])

        # Adding M2M table for field rooms on 'View'
        m2m_table_name = db.shorten_name(u'timetable_view_rooms')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('view', models.ForeignKey(orm[u'timetable.view'], null=False)),
            ('room', models.ForeignKey(orm[u'timetable.room'], null=False))
        ))
        db.create_unique(m2m_table_name, ['view_id', 'room_id'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'timetable_category')

        # Deleting model 'Room'
        db.delete_table(u'timetable_room')

        # Deleting model 'Person'
        db.delete_table(u'timetable_person')

        # Deleting model 'Role'
        db.delete_table(u'timetable_role')

        # Deleting model 'Programme'
        db.delete_table(u'timetable_programme')

        # Deleting model 'ProgrammeRole'
        db.delete_table(u'timetable_programmerole')

        # Deleting model 'View'
        db.delete_table(u'timetable_view')

        # Removing M2M table for field rooms on 'View'
        db.delete_table(db.shorten_name(u'timetable_view_rooms'))


    models = {
        u'timetable.category': {
            'Meta': {'ordering': "['title']", 'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'style': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1023'})
        },
        u'timetable.person': {
            'Meta': {'ordering': "['surname']", 'object_name': 'Person'},
            'anonymous': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '1023'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nick': ('django.db.models.fields.CharField', [], {'max_length': '1023', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '1023'})
        },
        u'timetable.programme': {
            'Meta': {'ordering': "['start_time', 'room']", 'object_name': 'Programme'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timetable.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'hilight': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'organizers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['timetable.Person']", 'through': u"orm['timetable.ProgrammeRole']", 'symmetrical': 'False'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timetable.Room']"}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1023'})
        },
        u'timetable.programmerole': {
            'Meta': {'object_name': 'ProgrammeRole'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timetable.Person']"}),
            'programme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timetable.Programme']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timetable.Role']"})
        },
        u'timetable.role': {
            'Meta': {'ordering': "['title']", 'object_name': 'Role'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'require_contact_info': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1023'})
        },
        u'timetable.room': {
            'Meta': {'ordering': "['order']", 'object_name': 'Room'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1023'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'timetable.view': {
            'Meta': {'ordering': "['order']", 'object_name': 'View'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'rooms': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['timetable.Room']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['timetable']