from rest_framework import viewsets, permissions, status
from rest_framework.serializers import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination


from app.models import Geofencing
from .serializers import GeofencingSerializer

import json


class GeofencingViewset(viewsets.ModelViewSet):

    queryset = Geofencing.objects.all()
    serializer_class = GeofencingSerializer

    def list(self, request):
        obj = Geofencing.objects.all()
        serializer = self.get_serializer(obj, many=True).data

        return Response(serializer, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):

        # print(type())
        # print(type(request.data.get("coordinates")))

        # response = super(GeofencingViewset, self).create(request, *args, **kwargs)
        name = request.data.get("name")
        coordinates = json.loads(request.data.get("coordinates"))
        center = request.data.get("center")

        obj = Geofencing(
            name=name,
            coordinates=coordinates,
            center=center
        ).save()

        serializer = self.get_serializer(obj).data

        return Response(status=status.HTTP_200_OK)

    def retrieve(self, request, **kwargs):
        # print(kwargs)
        obj = Geofencing.objects.get(pk=kwargs['pk'])

        serializer = self.get_serializer(obj).data

        return Response(serializer, status=status.HTTP_200_OK)


class GetGeofencing(APIView):

    def get(self, request):
        get_unit = request.query_params.get("unit", None)
        obj = Geofencing.objects.get(name=get_unit)
        serializer = GeofencingSerializer(obj).data
        return Response(serializer, status=status.HTTP_200_OK)