from rest_framework import viewsets, permissions, status
from rest_framework.serializers import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from datetime import datetime, timezone

from app import models
from . import serializers


class Pagination(PageNumberPagination):
    # page_size_query_param = 'page_size'
    # page_size = 25
    # max_page_size = 25
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10
    page_query_param = 'page'


class TransactionViewset(viewsets.ModelViewSet):
    pagination_class = Pagination
    queryset = models.Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer

    def get_object(self):
        queryset = models.Transaction.objects.all()
        try:
            return queryset.filter(pk=self.kwargs["pk"])
        except:
            raise ValidationError(
                {
                    "details": "not found or not exist"
                }
            )

    def list(self, request):
        # params = request.query_params.get("search", None)
        # station = request.query_params("station", None)
        get_obj = request.query_params.get("object", None)
        value = request.query_params.get("value", None)

        if get_obj == "person":
            by_person = models.Transaction.objects.filter(
                persons__full_name__contains=value).order_by("id")
            page = self.paginate_queryset(by_person)

            if page is not None:
                serializer = self.get_serializer(page, many=True).data
                return self.get_paginated_response(serializer)

        if get_obj == "unit":
            by_unit = models.Transaction.objects.filter(
                persons__person_unit__unit_code__contains=value).order_by("id")
            page = self.paginate_queryset(by_unit)

            if page is not None:
                serializer = self.get_serializer(page, many=True).data
                return self.get_paginated_response(serializer)

        if get_obj == "station":
            by_station = models.Transaction.objects.filter(
                persons__person_station__station_name__contains=value).order_by(
                "id")
            page = self.paginate_queryset(by_station)

            if page is not None:
                serializer = self.get_serializer(page, many=True).data
                return self.get_paginated_response(serializer)

        obj = models.Transaction.objects.all().order_by("id")

        page = self.paginate_queryset(obj)

        if page is not None:
            serializer = self.get_serializer(page, many=True).data
            return self.get_paginated_response(serializer)

        serializer = self.get_serializer(obj, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):

        if request.data.get("full_name"):
            full_name = request.data.pop("full_name")
            get_person = get_object_or_404(models.Person, full_name=full_name)
            request.data['persons'] = get_person.id

        response = super(TransactionViewset, self).create(request, *args,
                                                          **kwargs)

        return Response(response.data, status=status.HTTP_200_OK)


class UpdateLocation(APIView):

    def post(self, request):
        get_email = request.query_params.get("email", None)
        print(get_email)
        data = request.data
        print(data)

        if get_email:
            search_person = get_object_or_404(models.Person, email=get_email)

            get_transaction, created = models.Transaction.objects.update_or_create(
                persons=search_person,
                defaults={
                    'lat': data.get("lat"),
                    'lng': data.get("lng"),
                    'datetime': datetime.now(timezone.utc),
                    'modified_by': request.user
                })
            print(get_transaction)

        return Response(status=status.HTTP_200_OK)