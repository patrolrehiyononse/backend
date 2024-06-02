from rest_framework import viewsets, permissions, status
from rest_framework.serializers import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from app import models
# from . import serializers

from api.transaction import serializers as trans_serializer
from api.person import serializers as person_serializer


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
        obj = models.Person.objects.all()
        serializer = person_serializer.PersonSerializer(obj, many=True).data

        return Response(serializer, status=status.HTTP_200_OK)