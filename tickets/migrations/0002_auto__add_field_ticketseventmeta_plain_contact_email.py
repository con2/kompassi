# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'TicketsEventMeta.plain_contact_email'
        db.add_column(u'tickets_ticketseventmeta', 'plain_contact_email',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'TicketsEventMeta.plain_contact_email'
        db.delete_column(u'tickets_ticketseventmeta', 'plain_contact_email')


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
        u'core.venue': {
            'Meta': {'object_name': 'Venue'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'name_inessive': ('django.db.models.fields.CharField', [], {'max_length': '63'})
        },
        u'tickets.batch': {
            'Meta': {'object_name': 'Batch'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'delivery_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prepare_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'print_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'tickets.customer': {
            'Meta': {'object_name': 'Customer'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'allow_marketing_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'tickets.limitgroup': {
            'Meta': {'object_name': 'LimitGroup'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limit': ('django.db.models.fields.IntegerField', [], {})
        },
        u'tickets.order': {
            'Meta': {'object_name': 'Order'},
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tickets.Batch']", 'null': 'True', 'blank': 'True'}),
            'cancellation_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'confirm_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['tickets.Customer']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'payment_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'reference_number': ('django.db.models.fields.CharField', [], {'max_length': '31', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'tickets.orderproduct': {
            'Meta': {'object_name': 'OrderProduct'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'order_product_set'", 'to': u"orm['tickets.Order']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'order_product_set'", 'to': u"orm['tickets.Product']"})
        },
        u'tickets.product': {
            'Meta': {'object_name': 'Product'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'electronic_ticket': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'limit_groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['tickets.LimitGroup']", 'symmetrical': 'False', 'blank': 'True'}),
            'mail_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'notify_email': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'price_cents': ('django.db.models.fields.IntegerField', [], {}),
            'requires_shipping': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'tickets.ticketseventmeta': {
            'Meta': {'object_name': 'TicketsEventMeta'},
            'admin_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']"}),
            'contact_email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'due_days': ('django.db.models.fields.IntegerField', [], {'default': '14'}),
            'event': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'ticketseventmeta'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['core.Event']"}),
            'plain_contact_email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'reference_number_template': ('django.db.models.fields.CharField', [], {'default': "'{:04d}'", 'max_length': '31'}),
            'reservation_seconds': ('django.db.models.fields.IntegerField', [], {'default': '1800'}),
            'shipping_and_handling_cents': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'ticket_free_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'ticket_sales_ends': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'ticket_sales_starts': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'ticket_spam_email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['tickets']