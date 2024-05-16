from django.db import models


class BitcoinAddress(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=42, unique=True)
    balance = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    brl_balance = models.DecimalField(
        max_digits=20, decimal_places=8, default=0)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.address


class EthereumAddress(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=42, unique=True)
    balance = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    brl_balance = models.DecimalField(
        max_digits=20, decimal_places=8, default=0)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.address


class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    negotiation_code = models.CharField(max_length=10, unique=True)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    last_update = models.DateTimeField(auto_now=True)
    updated_value = models.DecimalField(
        max_digits=20, decimal_places=8, default=0)

    def __str__(self):
        return self.symbol


class Fii(models.Model):
    id = models.AutoField(primary_key=True)
    negotiation_code = models.CharField(max_length=10, unique=True)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    last_update = models.DateTimeField(auto_now=True)
    updated_value = models.DecimalField(
        max_digits=20, decimal_places=8, default=0)

    def __str__(self):
        return self.symbol


class TreasuryDirect(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.CharField(max_length=10, unique=True)
    indexer = models.CharField(max_length=50)
    quantity = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    deadline = models.DateTimeField()
    applied_value = models.DecimalField(
        max_digits=20, decimal_places=8, default=0)
    brute_value = models.DecimalField(
        max_digits=20, decimal_places=8, default=0)
    liquid_value = models.DecimalField(
        max_digits=20, decimal_places=8, default=0)
    updated_value = models.DecimalField(
        max_digits=20, decimal_places=8, default=0)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product
