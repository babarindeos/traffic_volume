from django.contrib import admin
from .models import Feature, Location, Cluster, Node, Vehicle, Traffic

# Register your models here.
admin.site.register(Feature)
admin.site.register(Location)
admin.site.register(Cluster)
admin.site.register(Node)
admin.site.register(Vehicle)
admin.site.register(Traffic)
