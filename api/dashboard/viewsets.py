from rest_framework import viewsets, permissions, status
from rest_framework.serializers import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from app import models
# from . import serializers

from api.transaction import serializers as trans_serializer
from api.person import serializers as person_serializer
from api.rank import serializers as rank_serializer
from api.unit import serializers as unit_serializer
from api.station import serializers as station_serializer


class DashboardTable(APIView):

    def get(self, request):
        search_station = request.query_params.get("station", None)
        all_trans = models.Transaction.objects.all()

        if search_station:
            get_trans = models.Transaction.objects.filter(
                persons__person_station__station_name=search_station)
            serialize = trans_serializer.TransactionSerializer(get_trans,
                                                               many=True).data
            return Response(serialize, status=status.HTTP_200_OK)

        trans_serialize = trans_serializer.TransactionSerializer(all_trans,
                                                                 many=True).data

        return Response(trans_serialize, status=status.HTTP_200_OK)

class PersonDropDown(APIView):

    def get(self, request):
        if request.user.is_superuser:
            obj = models.Person.objects.all()
        else:
            get_sub_unit = request.user.sub_unit
            obj = models.Person.objects.filter(
                person_sub_unit__sub_unit_description=get_sub_unit)
        serializer = person_serializer.PersonSerializer(obj, many=True).data

        return Response(serializer, status=status.HTTP_200_OK)

class DeleteAllPathTraces(APIView):

    def get(self, request):
        models.PathTrace.objects.all().delete()

        return Response("All Path Traces Deleted", status=status.HTTP_200_OK)