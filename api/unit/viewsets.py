from rest_framework import viewsets, permissions, status
from rest_framework.serializers import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

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

class UnitViewset(viewsets.ModelViewSet):
	pagination_class = Pagination
	queryset = models.Unit.objects.all()
	serializer_class = serializers.UnitSerializer

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
		obj = models.Unit.objects.all()

		page = self.paginate_queryset(obj)

		if page is not None:
			serializer = self.get_serializer(page, many=True).data
			return self.get_paginated_response(serializer)

		serializer = self.get_serializer(obj, many=True).data
		return Response(serializer, status=status.HTTP_200_OK)


	def create(self, request, *args, **kwargs):

		response = super(UnitViewset, self).create(request, *args, **kwargs)

		return Response(response.data, status=status.HTTP_200_OK)

	def update(self, request, pk=None, **kwargs):
		data = request.data

		get_unit = get_object_or_404(models.Unit, id=pk)

		get_unit.unit_code = data.get("unit_code")
		get_unit.description = data.get("description")
		get_unit.save()

		return Response(status=status.HTTP_200_OK)

	def destroy(self, request, pk=None):
		get_object_or_404(models.Unit, id=pk).delete()
		return Response(status=status.HTTP_200_OK)

class SubUnitViewset(viewsets.ModelViewSet):
	pagination_class = Pagination
	queryset = models.SubUnit.objects.all()
	serializer_class = serializers.SubUnitSerializer

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
		obj = models.SubUnit.objects.all()

		page = self.paginate_queryset(obj)

		if page is not None:
			serializer = self.get_serializer(page, many=True).data
			return self.get_paginated_response(serializer)

		serializer = self.get_serializer(obj, many=True).data
		return Response(serializer, status=status.HTTP_200_OK)

	def create(self, request, *args, **kwargs):

		if request.data.get("unit"):
			unit = request.data.pop("unit")
			get_unit = models.Unit.objects.get(unit_code=unit)
			request.data["units"] = get_unit.id

		response = super(SubUnitViewset, self).create(request, *args, **kwargs)

		return Response(response.data, status=status.HTTP_200_OK)

	def update(self, request, pk=None, **kwargs):

		data = request.data
		get_unit = None

		if data.get("unit"):
			unit = data.pop("unit")
			get_unit = get_object_or_404(models.Unit, unit_code=unit['unit_code'])


		get_subunit = get_object_or_404(models.SubUnit, id=pk)
		get_subunit.units = get_unit
		get_subunit.sub_unit_code = data.get("sub_unit_code")
		get_subunit.sub_unit_description = data.get("sub_unit_description")
		get_subunit.save()

		return Response(status=status.HTTP_200_OK)

	def destroy(self, request, pk=None):
		get_object_or_404(models.SubUnit, id=pk).delete()
		return Response(status=status.HTTP_200_OK)


class UnitDropDown(APIView):

	def get(self, request):

		obj = models.Unit.objects.all()
		serializer = serializers.UnitSerializer(obj, many=True).data
		return Response(serializer, status=status.HTTP_200_OK)

class SubUnitDropDown(APIView):

	def get(self, request):
		obj = models.SubUnit.objects.all()

		serializer = serializers.SubUnitSerializer(obj, many=True).data
		return Response(serializer, status=status.HTTP_200_OK)