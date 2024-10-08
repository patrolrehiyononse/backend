from rest_framework import viewsets, permissions, status
from rest_framework.serializers import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from app import models
from . import serializers


class Pagination(PageNumberPagination):
    # page_size_query_param = 'page_size'
    # page_size = 25
    # max_page_size = 25
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10
    page_query_param = 'page'


class StationViewset(viewsets.ModelViewSet):
    pagination_class = Pagination
    queryset = models.Station.objects.all()
    serializer_class = serializers.StationSerializer

    def get_object(self):
        queryset = models.Unit.objects.all()
        try:
            return queryset.filter(pk=self.kwargs["pk"])
        except:
            raise ValidationError(
                {
                    "details": "not found or not exist"
                }
            )

    def list(self, request):
        obj = models.Station.objects.all()

        page = self.paginate_queryset(obj)

        if page is not None:
            serializer = self.get_serializer(page, many=True).data
            return self.get_paginated_response(serializer)

        serializer = self.get_serializer(obj, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):

        if request.data.get("sub_unit"):
            sub_unit = request.data.pop("sub_unit")
            get_obj = models.SubUnit.objects.get(sub_unit_code=sub_unit)
            request.data["sub_unit"] = get_obj.id

        response = super(StationViewset, self).create(request, *args, **kwargs)

        return Response(response.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, **kwargs):
        data = request.data
        get_subunit = None
        if data.get("sub_unit"):
            get_value = data.pop("sub_unit")
            get_subunit = get_object_or_404(
                models.SubUnit, sub_unit_code=get_value['sub_unit_code'])

        get_station = get_object_or_404(models.Station, id=pk)
        get_station.sub_unit = get_subunit
        get_station.station_code = data.get("station_code")
        get_station.station_name = data.get("station_name")
        get_station.description = data.get("description")
        get_station.save()

        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        get_object_or_404(models.Station, id=pk).delete()
        return Response(status=status.HTTP_200_OK)

class StationDropDown(APIView):
    def get(self, request):

        obj = models.Station.objects.all()
        serializer = serializers.StationSerializer(obj, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)