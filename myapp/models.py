from django.db import models
from datetime import datetime

# Create your models here.
class Feature(models.Model):
    icon = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    details = models.CharField(max_length=500)


class Location(models.Model):
    name = models.CharField(max_length=500)
    date = models.DateTimeField(default=datetime.now, blank=True)


class Cluster(models.Model):
    name = models.CharField(max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='location')
    date = models.DateTimeField(default=datetime.now, blank= True)


class Node(models.Model):
    name = models.CharField(max_length=255)
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE, related_name='cluster')
    battery = models.IntegerField()
    fault = models.BooleanField()
    headship = models.BooleanField()
    date = models.DateTimeField(default=datetime.now, blank=True)


class Vehicle(models.Model):
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    plateno = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    date = models.DateTimeField(default=datetime.now, blank=True)


class Traffic(models.Model):
    identifier = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    cluster = models.CharField(max_length=255)
    headnode = models.CharField(max_length=255)
    vehicle  = models.CharField(max_length=255)
    date = models.DateTimeField(default=datetime.now, blank=True)

