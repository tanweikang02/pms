from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta, date

from django.db.models.query import QuerySet

# Create your models here.


class User(AbstractUser):
    contact = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.username} - {self.email}'


class Property(models.Model):
    name = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    availability = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.city}'

    def available_unit_count(self):
        unit_list = []
        units = Unit.objects.filter(property=self)
        for unit in units:
            if unit.ultimate_availability() == True:
                unit_list.append(unit)
        return len(unit_list)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'street': self.street,
            'city': self.city,
            'availability': self.availability,
            'timestamp': self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            'available_unit_count': self.available_unit_count()
        }


class Unit(models.Model):
    unit_id = models.CharField(max_length=255)
    floor = models.PositiveSmallIntegerField()
    rooms = models.PositiveSmallIntegerField()
    bathrooms = models.PositiveSmallIntegerField()
    size = models.IntegerField()
    with_balcony = models.BooleanField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='units')
    availability = models.BooleanField()
    optional_description = models.CharField(
        max_length=500, null=True, blank=True)

    def __str__(self):
        return f'{self.unit_id} - {self.property.name}'

    def ultimate_availability(self):
        try:
            Sale.objects.get(unit=self)
        except:
            bookings = Booking.objects.filter(unit=self)
            for booking in bookings:
                if booking.date <= date.today() and date.today() < booking.end_date():
                    return False
            if self.availability == True:
                return True
        return False

    def serialize(self):
        return {
            'id': self.id,
            'unit_id': self.unit_id,
            'floor': self.floor,
            'rooms': self.rooms,
            'bathrooms': self.bathrooms,
            'size': self.size,
            'with_balcony': self.with_balcony,
            'price': self.price,
            'property': self.property.id,
            'availability': self.availability,
            'optional_description': self.optional_description,
            'ultimate_availability': self.ultimate_availability()
        }


class Client(models.Model):
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f'{self.name} - {self.contact}'


class Booking(models.Model):
    customer = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='booking')
    salesperson = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='booking')
    unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name='booking')
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Booking - {self.salesperson.username}({self.customer})'

    def end_date(self):
        return self.date + timedelta(7)


class Sale(models.Model):
    customer = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='sale')
    unit = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name='sale')
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name='sale')
    salesperson = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sale')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Sale - {self.unit.unit_id}({self.unit.property.name}) made by {self.salesperson}'

    def amount(self):
        return self.unit.price


class Note(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='note')
    salesperson = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='note')
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Note - {self.salesperson.username} - {self.property.name}'


class BookingFile(models.Model):
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='booking/')
    timestamp = models.DateTimeField(auto_now_add=True)


class SaleFile(models.Model):
    sale = models.ForeignKey(
        Sale, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='sale/')
    timestamp = models.DateTimeField(auto_now_add=True)
