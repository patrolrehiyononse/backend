from rest_framework import viewsets, permissions, status
from rest_framework.serializers import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from app import models
from . import serializers

from rest_framework.views import APIView


class Pagination(PageNumberPagination):
    # page_size_query_param = 'page_size'
    # page_size = 25
    # max_page_size = 25
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10
    page_query_param = 'page'


class PersonViewset(viewsets.ModelViewSet):
    queryset = models.Person.objects.all()
    pagination_class = Pagination
    serializer_class = serializers.PersonSerializer

    def get_object(self):
        queryset = models.Rank.objects.all()
        try:
            return queryset.filter(pk=self.kwargs["pk"])
        except:
            raise ValidationError(
                {
                    "details": "not found or not exist"
                }
            )

    def list(self, request):
        obj = None

        if request.user.is_superuser:
            obj = models.Person.objects.all()
        else:
            get_sub_unit = request.user.sub_unit
            obj = models.Person.objects.filter(
                person_sub_unit__sub_unit_description=get_sub_unit)

        page = self.paginate_queryset(obj)

        if page is not None:
            serializer = self.get_serializer(page, many=True).data
            return self.get_paginated_response(serializer)

        serializer = self.get_serializer(obj, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):

        if request.data.get("rank"):
            rank = request.data.pop("rank")
            get_rank = get_object_or_404(models.Rank, rank_code=rank)
            request.data['person_rank'] = get_rank.pk

        if request.data.get("unit"):
            unit = request.data.pop("unit")
            get_unit = get_object_or_404(models.Unit, unit_code=unit)
            request.data['person_unit'] = get_unit.pk

        if request.data.get("sub_unit"):
            sub_unit = request.data.pop("sub_unit")
            get_sub_unit = get_object_or_404(models.SubUnit, sub_unit_code=sub_unit)
            request.data['person_sub_unit'] = get_sub_unit.pk

        if request.data.get("station"):
            station = request.data.pop("station")
            get_station = get_object_or_404(models.Station, station_code=station)
            request.data['person_station'] = get_station.pk

        User = get_user_model()


        response = super(PersonViewset, self).create(request, *args, **kwargs)

        User.objects.create_user(
            username=request.data.get("full_name").lower().replace(" ", "_"),
            email=request.data.get("email"),
            password="123",
            role="user",
        )

        return Response(response.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, **kwargs):
        data = request.data
        get_rank = None
        get_unit = None
        get_subunit = None
        get_station = None

        person = models.Person.objects.get(pk=pk)

        if data.get("rank"):
            get_rank = models.Rank.objects.get(rank_code=data.get("rank")['rank_code'])
        if data.get("unit"):
            get_unit = models.Unit.objects.get(description=data.get("unit")['description'])
        if data.get("sub_unit"):
            get_subunit = models.SubUnit.objects.get(sub_unit_description=data.get("sub_unit")['sub_unit_description'])
        if data.get("station"):
            get_station = models.Station.objects.get(description=data.get("station")['description'])

        person.full_name = data.get("full_name")
        person.email = data.get("email")
        person.person_rank = get_rank
        person.person_unit = get_unit
        person.person_sub_unit = get_subunit
        person.person_station = get_station
        person.save()

        response = serializers.PersonSerializer(person)

        return Response(response.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):

        get_person = get_object_or_404(models.Person, id=pk)
        get_person.delete()

        return Response(status=status.HTTP_200_OK)


