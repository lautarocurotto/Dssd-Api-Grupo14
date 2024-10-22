from django.db import models
from django.contrib.auth.models import User

class Material(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Deposit(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    materials = models.ManyToManyField(Material, related_name='providers', blank=True)

class Order(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    deposit = models.ForeignKey(Deposit, on_delete=models.CASCADE)
    reserved = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} for {self.material.name}"
