from rest_framework import viewsets, permissions, status
from rest_framework.serializers import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from datetime import datetime, timezone
from rest_framework.decorators import action

from app import models
from . import serializers


class Pagination(PageNumberPagination):
    page_size = 10
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
        obj = None

        if request.user.is_superuser:
            obj = models.Transaction.objects.all().order_by("id")
        else:
            get_sub_unit = request.user.sub_unit
            obj = models.Transaction.objects.filter(
                persons__person_sub_unit__sub_unit_description=get_sub_unit)


        if get_obj == "person":
            by_person = obj.filter(
                persons__full_name__contains=value).order_by("id")
            page = self.paginate_queryset(by_person)

            if page is not None:
                serializer = self.get_serializer(page, many=True).data
                return self.get_paginated_response(serializer)

        if get_obj == "unit":
            by_unit = obj.filter(
                persons__person_unit__unit_code__contains=value).order_by("id")
            page = self.paginate_queryset(by_unit)

            if page is not None:
                serializer = self.get_serializer(page, many=True).data
                return self.get_paginated_response(serializer)

        if get_obj == "station":
            by_station = obj.filter(
                persons__person_station__station_name__contains=value).order_by(
                "id")
            page = self.paginate_queryset(by_station)

            if page is not None:
                serializer = self.get_serializer(page, many=True).data
                return self.get_paginated_response(serializer)



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
        data = request.data

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

class DeployedUnitsViewSet(viewsets.ModelViewSet):
    queryset = models.DeployedUnits.objects.all()
    serializer_class = serializers.DeployedUnitsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = models.DeployedUnits.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_path='update-arrival-status')
    def update_arrival_status(self, request, pk=None):
        person_id = request.data.get('person_id')
        is_arrived = request.data.get('is_arrived')

        if person_id is None or is_arrived is None:
            return Response(
                {'error': 'person_id and is_arrived fields are required.'},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            deployment_person = models.DeployedUnitPerson.objects.get(
                deployed_unit_id=pk, person_id=person_id)
            deployment_person.is_arrived = is_arrived
            deployment_person.save()

            # Check if all persons have arrived
            deployment = models.DeployedUnits.objects.get(pk=pk)
            all_arrived = all(person.is_arrived for person in
                              deployment.deployedunitperson_set.all())

            if all_arrived:
                deployment.is_done = True
                deployment.save()
            else:
                deployment.is_done = False
                deployment.save()


            serializer = self.get_serializer(deployment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.DeployedUnitPerson.DoesNotExist:
            return Response({'error': 'DeployedUnitPerson not found.'},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {'error': 'An error occurred while updating arrival status.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='by-person')
    def get_by_person(self, request):
        person_id = request.query_params.get('person_id')
        if not person_id:
            return Response(
                {'error': 'person_id query parameter is required.'},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            deployed_units = models.DeployedUnits.objects.filter(
                persons__id=person_id, is_done=False)
            serializer = self.get_serializer(deployed_units, many=True)
            return Response(serializer.data)
        except models.DeployedUnits.DoesNotExist:
            return Response(
                {'error': 'No deployed units found for the given person_id.'},
                status=status.HTTP_404_NOT_FOUND)