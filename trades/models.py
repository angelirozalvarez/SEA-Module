from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Trader(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Bank(models.Model):
    bank_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.bank_name}"

class Trade(models.Model):
    TRADE_NAME = (
        ('Bond Asset Swap', 'Bond Asset Swap'),
        ('Bond Outright', 'Bond Outright'),
        ('Bond Butterfly', 'Bond Butterfly'),
        ('Bond Switch', 'Bond Switch'),
        ('Irs Outright', 'Irs Outright'),
        ('Irs Curve', 'Irs Curve'),
        ('Irs Butterfly', 'Irs Butterfly'),
        ('Invoices Spread', 'Invoices Spread'),
        ('Generic Enquiry', 'Generic Enquiry'),
        ('Swap Butterfly', 'Swap Butterfly'),
        ('Swap Curve', 'Swap Curve'),
        ('Swap List', 'Swap List'),
        ('Swap Outright', 'Swap Outright'),
    )

    STATUS = (
        ('Accepted', 'Accepted'),
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected'),
    )

    trade_name = models.CharField(max_length=30, choices=TRADE_NAME)
    status = models.CharField(max_length=15, choices=STATUS)
    status_comments = models.TextField(blank=True)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(1000)])
    price = models.DecimalField(validators=[MinValueValidator(500), MaxValueValidator(1000000)], decimal_places=2, max_digits=9)
    datetime = models.DateTimeField(auto_now_add=True)
    trader = models.ForeignKey(Trader, on_delete=models.SET_NULL, null=True)
    bank = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.trade_name}"