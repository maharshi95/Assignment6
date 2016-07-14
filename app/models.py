# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from django.db import models


class Address(models.Model):
    address_id = models.BigIntegerField(primary_key=True)
    street1 = models.CharField(max_length=45, blank=True, null=True)
    street2 = models.CharField(max_length=45, blank=True, null=True)
    city = models.CharField(max_length=45, blank=True, null=True)
    state = models.CharField(max_length=45, blank=True, null=True)
    country = models.CharField(max_length=45, blank=True, null=True)
    zipcode = models.CharField(max_length=45, blank=True, null=True)
    mobile = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Address'


class Category(models.Model):
    category_id = models.BigIntegerField(primary_key=True,auto_created=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return "C" + str(self.category_id) + ": " + str(self.name)

    class Meta:
        managed = False
        db_table = 'Category'


class Customer(models.Model):
    customer_id = models.BigIntegerField(primary_key=True)
    email_id = models.CharField(unique=True, max_length=45)
    company_name = models.CharField(max_length=45, blank=True, null=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45, blank=True, null=True)
    contact = models.CharField(max_length=45, blank=True, null=True)
    current_add_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Customer'


class CustomerAddress(models.Model):
    customer = models.ForeignKey(Customer, models.DO_NOTHING)
    add_code = models.ForeignKey(Address, models.DO_NOTHING, db_column='add_code')

    class Meta:
        managed = False
        db_table = 'Customer_Address'
        unique_together = (('customer', 'add_code'),)


class Orderdetails(models.Model):
    order = models.ForeignKey('Orders', models.DO_NOTHING)
    product = models.ForeignKey('Product', models.DO_NOTHING)
    quantity = models.BigIntegerField()
    sell_price = models.FloatField()

    class Meta:
        managed = False
        db_table = 'OrderDetails'
        unique_together = (('order', 'product'),)


class Orders(models.Model):
    order_id = models.BigIntegerField(primary_key=True)
    customer_id = models.BigIntegerField(blank=True, null=True)
    time_created = models.DateTimeField()
    order_status = models.CharField(max_length=45, blank=True, null=True)
    payment_mode = models.CharField(max_length=45, blank=True, null=True)
    payment_status = models.CharField(max_length=45, blank=True, null=True)
    deleted = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Orders'


class Product(models.Model):
    product_id = models.BigIntegerField(primary_key=True)
    category_id = models.BigIntegerField()
    product_code = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    buy_price = models.FloatField()
    sell_price = models.FloatField()
    quantity = models.BigIntegerField()
    deleted = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "P" + str(self.product_id) + ": " + str(self.product_code)

    class Meta:
        managed = False
        db_table = 'Product'


class AuditLog(models.Model):
    audit_id = models.AutoField(primary_key=True)
    time_created = models.DateTimeField(blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    params = models.CharField(max_length=200, blank=True, null=True)
    response_code = models.BigIntegerField(blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    request_type = models.CharField(max_length=45, blank=True, null=True)
    request_duration_ms = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audit_log'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'
