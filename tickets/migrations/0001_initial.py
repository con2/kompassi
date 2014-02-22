# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Batch'
        db.create_table('ticket_sales_batch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('print_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('prepare_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('delivery_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('ticket_sales', ['Batch'])

        # Adding model 'Product'
        db.create_table('ticket_sales_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('mail_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('classname', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('sell_limit', self.gf('django.db.models.fields.IntegerField')()),
            ('price_cents', self.gf('django.db.models.fields.IntegerField')()),
            ('requires_shipping', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('available', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('ilmoitus_mail', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('ticket_sales', ['Product'])

        # Adding model 'School'
        db.create_table('ticket_sales_school', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ticket_sales.Product'])),
            ('max_people', self.gf('django.db.models.fields.IntegerField')()),
            ('priority', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('ticket_sales', ['School'])

        # Adding model 'Customer'
        db.create_table('ticket_sales_customer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
        ))
        db.send_create_signal('ticket_sales', ['Customer'])

        # Adding model 'Order'
        db.create_table('ticket_sales_order', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['ticket_sales.Customer'], unique=True, null=True, blank=True)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('confirm_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('ip_address', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('payment_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('cancellation_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('batch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ticket_sales.Batch'], null=True, blank=True)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ticket_sales.School'], null=True, blank=True)),
        ))
        db.send_create_signal('ticket_sales', ['Order'])

        # Adding model 'OrderProduct'
        db.create_table('ticket_sales_orderproduct', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='order_product_set', to=orm['ticket_sales.Order'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='order_product_set', to=orm['ticket_sales.Product'])),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('ticket_sales', ['OrderProduct'])


    def backwards(self, orm):
        # Deleting model 'Batch'
        db.delete_table('ticket_sales_batch')

        # Deleting model 'Product'
        db.delete_table('ticket_sales_product')

        # Deleting model 'School'
        db.delete_table('ticket_sales_school')

        # Deleting model 'Customer'
        db.delete_table('ticket_sales_customer')

        # Deleting model 'Order'
        db.delete_table('ticket_sales_order')

        # Deleting model 'OrderProduct'
        db.delete_table('ticket_sales_orderproduct')


    models = {
        'ticket_sales.batch': {
            'Meta': {'object_name': 'Batch'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'delivery_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prepare_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'print_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'ticket_sales.customer': {
            'Meta': {'object_name': 'Customer'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'ticket_sales.order': {
            'Meta': {'object_name': 'Order'},
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ticket_sales.Batch']", 'null': 'True', 'blank': 'True'}),
            'cancellation_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'confirm_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ticket_sales.Customer']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'payment_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ticket_sales.School']", 'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'ticket_sales.orderproduct': {
            'Meta': {'object_name': 'OrderProduct'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'order_product_set'", 'to': "orm['ticket_sales.Order']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'order_product_set'", 'to': "orm['ticket_sales.Product']"})
        },
        'ticket_sales.product': {
            'Meta': {'object_name': 'Product'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'classname': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ilmoitus_mail': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'mail_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price_cents': ('django.db.models.fields.IntegerField', [], {}),
            'requires_shipping': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sell_limit': ('django.db.models.fields.IntegerField', [], {})
        },
        'ticket_sales.school': {
            'Meta': {'object_name': 'School'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_people': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'priority': ('django.db.models.fields.IntegerField', [], {}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ticket_sales.Product']"})
        }
    }

    complete_apps = ['ticket_sales']