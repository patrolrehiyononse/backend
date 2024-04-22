from rest_framework import viewsets, permissions, status
from rest_framework.serializers import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination


from app.models import Geofencing
from .serializers import GeofencingSerializer


class GeofencingViewset(viewsets.ModelViewSet):

    queryset = Geofencing.objects.all()
    serializer_class = GeofencingSerializer

    def list(self, request):
        obj = Geofencing.objects.all()
        serializer = self.get_serializer(obj, many=True).data

        return Response(serializer, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):

        response = super(GeofencingViewset, self).create(request, *args, **kwargs)

        return Response(response.data, status=status.HTTP_200_OK)

    def retrieve(self, request, **kwargs):
        obj = Geofencing.objects.get(pk=kwargs['pk'])

        serializer = self.get_serializer(obj).data

        return Response(serializer, status=status.HTTP_200_OK)

