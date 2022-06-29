from rest_framework import filters
from rest_framework import pagination, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Word, Course
from .serializers import WordSerializer, CourseSerializer


class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "count"

    def get_paginated_response(self, data):
        return Response({"total": self.page.paginator.count, "data": data})


class WordViewSet(viewsets.ModelViewSet):
    serializer_class = WordSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    filter_backends = [filters.OrderingFilter]
    ordering_fields = "__all__"

    def get_queryset(self):
        return Word.objects.course(self.request.user.student, self.kwargs["course_pk"])

    @action(detail=False)
    def practice(self, request, *args, **kwargs):
        words = self.get_queryset().order_by("?")
        serializer = self.get_serializer(words, many=True)
        return Response(serializer.data)


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    filter_backends = [filters.OrderingFilter]
    ordering_fields = "__all__"

    def get_queryset(self):
        return Course.objects.student(self.request.user.student)
