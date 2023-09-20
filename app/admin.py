from django.contrib import admin
from . import models


# Register your models here.
admin.site.register(models.Unit)
admin.site.register(models.Rank)
admin.site.register(models.Person)
admin.site.register(models.Transaction)
admin.site.register(models.SubUnit)
admin.site.register(models.Station)