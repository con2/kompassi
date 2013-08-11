# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'timetable_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'timetable', ['Tag'])

        # Adding M2M table for field tags on 'Programme'
        m2m_table_name = db.shorten_name(u'timetable_programme_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('programme', models.ForeignKey(orm[u'timetable.programme'], null=False)),
            ('tag', models.ForeignKey(orm[u'timetable.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['programme_id', 'tag_id'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table(u'timetable_tag')

        # Removing M2M table for field tags on 'Programme'
        db.delete_table(db.shorten_name(u'timetable_programme_tags'))


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
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['timetable.Tag']", 'symmetrical': 'False'}),
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
        u'timetable.tag': {
            'Meta': {'ordering': "['order']", 'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '15'})
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