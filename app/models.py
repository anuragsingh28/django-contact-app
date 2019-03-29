from django.db import models
from django.utils.timezone import datetime
from django.contrib.auth.models import User
# Create your models here.


class Contact(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    phone = models.IntegerField()
    info = models.CharField(max_length=50)
    gender = models.CharField(max_length=20, choices=(
        ('male', 'Male'),
        ('female', 'Female'),
    ))
    image = models.ImageField(upload_to='images/', blank=True)
    date_added = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.name
