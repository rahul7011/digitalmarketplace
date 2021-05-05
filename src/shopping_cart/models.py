from django.db import models
from django.conf import settings
from books.models import Book
from django.db.models import Sum


class OrderItem(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE)

    def __str__(self):
        return self.book.title

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField('OrderItem')
    ref_code=models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

    def get_total(self):
        return self.items.all().aggregate(order_total=Sum('book__price'))['order_total']

class Payment(models.Model):
    order=models.ForeignKey('Order',on_delete=models.CASCADE)
    total_amount=models.FloatField()
    date_paid=models.DateTimeField(auto_now_add=True)
    stripe_charge_id=models.CharField(max_length=100)
    
    def __str__(self):
        return self.stripe_charge_id
    