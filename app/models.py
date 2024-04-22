from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.
class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_creator",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_updater",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

class Unit(BaseModel):
    unit_code = models.CharField(max_length=255, null=True, blank=True)
    abbreviation = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.description + " - " + self.unit_code


class Rank(BaseModel):
    rank_code = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.rank_code + " - " + self.rank_code


class Person(BaseModel):
    account_number = models.IntegerField(null=True, blank=True)
    full_name = models.CharField(max_length=256, null=True, blank=True)
    # last_name = models.CharField(max_length=255, null=True, blank=True)
    # first_name = models.CharField(max_length=255, null=True, blank=True)
    # middle_name = models.CharField(max_length=255, null=True, blank=True)
    person_unit = models.ForeignKey(Unit, null=True, blank=True,
                                    on_delete=models.DO_NOTHING)
    person_rank = models.ForeignKey(Rank, null=True, blank=True,
                                    on_delete=models.DO_NOTHING)
    person_station = models.ForeignKey("Station", null=True, blank=True,
                                       on_delete=models.DO_NOTHING)
    email = models.EmailField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.full_name + " - " + self.email


class Transaction(BaseModel):
    persons = models.ForeignKey(Person, null=True, on_delete=models.DO_NOTHING,
                                blank=True)
    lat = models.CharField(max_length=255, null=True, blank=True)
    lng = models.CharField(max_length=255, null=True, blank=True)
    datetime = models.DateTimeField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=False)


class SubUnit(BaseModel):
    units = models.ForeignKey(Unit, null=True, blank=True,
                              on_delete=models.DO_NOTHING)
    sub_unit_code = models.CharField(max_length=255, null=True, blank=True)
    sub_unit_description = models.CharField(max_length=255, null=True,
                                            blank=True)
    abbreviation = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.sub_unit_description + " - " + self.sub_unit_code


class Station(BaseModel):
    sub_unit = models.ForeignKey(SubUnit, null=True, blank=True,
                                 on_delete=models.CASCADE)
    station_code = models.CharField(max_length=255, null=True, blank=True)
    station_name = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        # return self.station_name + " - " + self.description
        return self.station_name

class Geofencing(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    coordinates = models.CharField(max_length=255, null=True, blank=True)
    center = models.CharField(max_length=255, null=True, blank=True)
