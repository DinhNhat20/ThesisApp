from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, generics, status, parsers
from rest_framework.decorators import action
from rest_framework.response import Response
from theses.models import User, DepartmentAdmin, Lecturer, Student, Department, Major, SchoolYear, Position, Council, \
    CouncilDetail, Role, Thesis, ThesisScore, ScoreComponent, ScoreColumn, ScoreDetail, Supervisor, Notification, \
    NotificationUser
from theses import serializers, paginators


class RoleViewSet(viewsets.ModelViewSet):  #ModelViewSet: lấy tất cả các action CRUD
    queryset = Role.objects.all()
    serializer_class = serializers.RoleSerializer


class ThesisViewSet(viewsets.ModelViewSet):
    queryset = Thesis.objects.all()
    serializer_class = serializers.ThesisSerializer


class CouncilViewSet(viewsets.ModelViewSet):
    queryset = Council.objects.all()
    serializer_class = serializers.CouncilSerializer


class DepartmentAdminViewSet(viewsets.ModelViewSet):
    queryset = DepartmentAdmin.objects.all()
    serializer_class = serializers.DepartmentAdminSerializer


class LecturerViewSet(viewsets.ModelViewSet):
    queryset = Lecturer.objects.all()
    serializer_class = serializers.LecturerSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = serializers.DepartmentSerializer


class MajorViewSet(viewsets.ModelViewSet):
    queryset = Major.objects.all()
    serializer_class = serializers.MajorSerializer


class SchoolYearViewSet(viewsets.ModelViewSet):
    queryset = SchoolYear.objects.all()
    serializer_class = serializers.SchoolYearSerializer


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = serializers.PositionSerializer


class SupervisorViewSet(viewsets.ModelViewSet):
    queryset = Supervisor.objects.all()
    serializer_class = serializers.SupervisorSerializer


class CouncilDetailViewSet(viewsets.ModelViewSet):
    queryset = CouncilDetail.objects.all()
    serializer_class = serializers.CouncilDetailSerializer


class ThesisScoreViewSet(viewsets.ModelViewSet):
    queryset = ThesisScore.objects.all()
    serializer_class = serializers.ThesisScoreSerializer


class ScoreComponentViewSet(viewsets.ModelViewSet):
    queryset = ScoreComponent.objects.all()
    serializer_class = serializers.ScoreComponentSerializer


class ScoreColumnViewSet(viewsets.ModelViewSet):
    queryset = ScoreColumn.objects.all()
    serializer_class = serializers.ScoreColumnSerializer


class ScoreDetailViewSet(viewsets.ModelViewSet):
    queryset = ScoreDetail.objects.all()
    serializer_class = serializers.ScoreDetailSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = serializers.NotificationSerializer


class NotificationUserViewSet(viewsets.ModelViewSet):
    queryset = NotificationUser.objects.all()
    serializer_class = serializers.NotificationSerializer


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser, ]

# def index(request):
#     return HttpResponse("Thesis app")
