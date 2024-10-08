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

class RankViewset(viewsets.ModelViewSet):
	pagination_class = Pagination
	queryset = models.Rank.objects.all()
	serializer_class = serializers.RankSerializer

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
		obj = models.Rank.objects.all()

		page = self.paginate_queryset(obj)

		if page is not None:
			serializer = self.get_serializer(page, many=True).data
			return self.get_paginated_response(serializer)

		serializer = self.get_serializer(obj, many=True).data
		return Response(serializer, status=status.HTTP_200_OK)


	def create(self, request, *args, **kwargs):

		response = super(RankViewset, self).create(request, *args, **kwargs)

		return Response(response.data, status=status.HTTP_200_OK)

	def update(self, request, pk=None, **kwargs):
		data = request.data

		get_rank = get_object_or_404(models.Rank, id=pk)

		get_rank.rank_code = data.get("rank_code")
		get_rank.description = data.get("description")
		get_rank.save()

		return Response(status=status.HTTP_200_OK)

	def destroy(self, request, pk=None):
		get_object_or_404(models.Rank, id=pk).delete()
		return Response(status=status.HTTP_200_OK)

class RankDropDown(APIView):

	def get(self, request):

		obj = models.Rank.objects.all()
		serializer = serializers.RankSerializer(obj, many=True).data
		return Response(serializer, status=status.HTTP_200_OK)