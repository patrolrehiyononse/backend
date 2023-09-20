from rest_framework import viewsets, permissions, status
from rest_framework.serializers import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

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

		response = super(SubUnitViewset, self).create(request, *args, **kwargs)

		return Response(response.data, status=status.HTTP_200_OK)