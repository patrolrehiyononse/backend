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
    person_unit = models.ForeignKey(Unit, null=True, blank=True,
                                    on_delete=models.CASCADE)
    person_rank = models.ForeignKey(Rank, null=True, blank=True,
                                    on_delete=models.CASCADE)
    person_station = models.ForeignKey("Station", null=True, blank=True,
                                       on_delete=models.CASCADE)
    person_sub_unit = models.ForeignKey("SubUnit", null=True, blank=True,
                                       on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.full_name + " - " + self.email


class PathTrace(BaseModel):
    persons = models.ForeignKey(Person, null=True, blank=True,
                               on_delete=models.CASCADE)
    lat = models.CharField(max_length=255, null=True, blank=True)
    lng = models.CharField(max_length=255, null=True, blank=True)
    datetime = models.DateTimeField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.persons.full_name


class Transaction(BaseModel):
    persons = models.ForeignKey(Person, null=True, on_delete=models.CASCADE,
                                blank=True)
    lat = models.CharField(max_length=255, null=True, blank=True)
    lng = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    datetime = models.DateTimeField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=False)


class SubUnit(BaseModel):
    units = models.ForeignKey(Unit, null=True, blank=True,
                              on_delete=models.CASCADE)
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
    # coordinates = models.CharField(null=True, blank=True)
    # coordinates = models.TextField(null=True, blank=True)
    coordinates = models.JSONField(null=True, blank=True)
    center = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name + " " + str(self.pk)

class DeployedUnitPerson(models.Model):
    deployed_unit = models.ForeignKey('DeployedUnits', on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    is_arrived = models.BooleanField(null=True, blank=True, default=False)


class DeployedUnits(BaseModel):
    persons = models.ManyToManyField(Person, through='DeployedUnitPerson')
    destination = models.CharField(max_length=500, null=True, blank=True)
    deployment_name = models.CharField(max_length=255, null=True, blank=True)
    coordinates = models.CharField(max_length=255, null=True, blank=True)
    is_done = models.BooleanField(null=True, blank=True, default=False)

    # def __str__(self):
    #     return self.deployment_name