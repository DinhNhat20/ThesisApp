from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, generics, status, parsers
from rest_framework.decorators import action
from rest_framework.response import Response
from theses.models import User, Admin, Lecturer, Student, Faculty, Major, SchoolYear, Position, Council, CouncilDetail, \
    Role, Thesis, ThesisScore, ScoreComponent, ScoreColumn, ScoreDetail, Supervisor
from theses import serializers, paginators


class RoleViewSet(viewsets.ModelViewSet):  #ModelViewSet: lấy tất cả các action CRUD
    queryset = Role.objects.all()
    serializer_class = serializers.RoleSerializer


class ThesisViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Thesis.objects.all()
    serializer_class = serializers.ThesisSerializer


class CouncilViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Council.objects.all()
    serializer_class = serializers.CouncilSerializer


class LecturerViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Lecturer.objects.all()
    serializer_class = serializers.LecturerSerializer


class StudentViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer


class FacultyViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Faculty.objects.all()
    serializer_class = serializers.FacultySerializer


class MajorViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Major.objects.all()
    serializer_class = serializers.MajorSerializer


class SchoolYearViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = SchoolYear.objects.all()
    serializer_class = serializers.SchoolYearSerializer


class PositionViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Position.objects.all()
    serializer_class = serializers.PositionSerializer


class SupervisorViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Supervisor.objects.all()
    serializer_class = serializers.SupervisorSerializer

class UserViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser, ]

# def index(request):
#     return HttpResponse("Thesis app")
