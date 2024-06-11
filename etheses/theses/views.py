from django.contrib.auth import authenticate, login
from django.db.models import Avg, Count
from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse
from rest_framework import viewsets, generics, status, parsers, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from theses.models import User, DepartmentAdmin, Lecturer, Student, Department, Major, SchoolYear, Position, Council, \
    CouncilDetail, Role, Thesis, ThesisScore, ScoreComponent, ScoreColumn, ScoreDetail, Supervisor, Notification, \
    NotificationUser
from theses import serializers, paginators
from theses.serializers import CouncilSerializer


class RoleViewSet(viewsets.ModelViewSet):  #ModelViewSet: lấy tất cả các action CRUD
    queryset = Role.objects.all()
    serializer_class = serializers.RoleSerializer


class ThesisViewSet(viewsets.ModelViewSet):
    queryset = Thesis.objects.all()
    serializer_class = serializers.ThesisSerializer
    pagination_class = paginators.ThesisPaginator

    def get_queryset(self):
        queryset = self.queryset

        if self.action.__eq__('list'):
            q = self.request.query_params.get('q')
            if q:
                queryset = queryset.filter(name__icontains=q)

            major = self.request.query_params.get('major')
            if major:
                queryset = queryset.filter(major=major)

        return queryset


class CouncilViewSet(viewsets.ModelViewSet):
    queryset = Council.objects.all()
    serializer_class = serializers.CouncilSerializer
    pagination_class = paginators.commonPaginator


class DepartmentAdminViewSet(viewsets.ModelViewSet):
    queryset = DepartmentAdmin.objects.all()
    serializer_class = serializers.DepartmentAdminSerializer
    pagination_class = paginators.commonPaginator


class LecturerViewSet(viewsets.ModelViewSet):
    queryset = Lecturer.objects.all()
    serializer_class = serializers.LecturerSerializer
    pagination_class = paginators.commonPaginator

    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset

        if self.action.__eq__('list'):
            q = self.request.query_params.get('q')
            if q:
                queryset = queryset.filter(name__icontains=q)

            user = self.request.query_params.get('user')
            if user:
                queryset = queryset.filter(user=user)

        return queryset


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer
    pagination_class = paginators.commonPaginator

    def get_queryset(self):
        queryset = self.queryset

        if self.action.__eq__('list'):
            q = self.request.query_params.get('q')
            if q:
                queryset = queryset.filter(full_name__icontains=q)

            code = self.request.query_params.get('code')
            if code:
                queryset = queryset.filter(code__icontains=code)

        return queryset


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    pagination_class = paginators.commonPaginator

    def get_queryset(self):
        queryset = self.queryset

        if self.action.__eq__('list'):
            q = self.request.query_params.get('q')
            if q:
                queryset = queryset.filter(name__icontains=q)

            code = self.request.query_params.get('code')
            if code:
                queryset = queryset.filter(code__icontains=code)

        return queryset


class MajorViewSet(viewsets.ModelViewSet):
    queryset = Major.objects.all()
    serializer_class = serializers.MajorSerializer
    pagination_class = paginators.commonPaginator

    def get_queryset(self):
        queryset = self.queryset

        if self.action.__eq__('list'):
            q = self.request.query_params.get('q')
            if q:
                queryset = queryset.filter(name__icontains=q)

            code = self.request.query_params.get('code')
            if code:
                queryset = queryset.filter(code__icontains=code)

        return queryset


class SchoolYearViewSet(viewsets.ModelViewSet):
    queryset = SchoolYear.objects.all()
    serializer_class = serializers.SchoolYearSerializer
    pagination_class = paginators.commonPaginator


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = serializers.PositionSerializer
    pagination_class = paginators.commonPaginator


class SupervisorViewSet(viewsets.ModelViewSet):
    queryset = Supervisor.objects.all()
    serializer_class = serializers.SupervisorSerializer
    pagination_class = paginators.commonPaginator


class CouncilDetailViewSet(viewsets.ModelViewSet):
    queryset = CouncilDetail.objects.all()
    serializer_class = serializers.CouncilDetailSerializer
    pagination_class = paginators.commonPaginator


class ThesisScoreViewSet(viewsets.ModelViewSet):
    queryset = ThesisScore.objects.all()
    serializer_class = serializers.ThesisScoreSerializer
    pagination_class = paginators.commonPaginator


class ScoreComponentViewSet(viewsets.ModelViewSet):
    queryset = ScoreComponent.objects.all()
    serializer_class = serializers.ScoreComponentSerializer
    pagination_class = paginators.commonPaginator


class ScoreColumnViewSet(viewsets.ModelViewSet):
    queryset = ScoreColumn.objects.all()
    serializer_class = serializers.ScoreColumnSerializer
    pagination_class = paginators.commonPaginator


class ScoreDetailViewSet(viewsets.ModelViewSet):
    queryset = ScoreDetail.objects.all()
    serializer_class = serializers.ScoreDetailSerializer
    pagination_class = paginators.commonPaginator


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = serializers.NotificationSerializer
    pagination_class = paginators.commonPaginator


class NotificationUserViewSet(viewsets.ModelViewSet):
    queryset = NotificationUser.objects.all()
    serializer_class = serializers.NotificationSerializer
    pagination_class = paginators.commonPaginator


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser, ]

    def get_permissions(self):
        if self.action in ['get_current_user']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get', 'patch'], url_path='current-user', detail=False)
    def get_current_user(self, request):
        user = request.user
        if request.method.__eq__('PATCH'):
            for k, v in request.data.items():
                setattr(user, k, v)
            user.save()

        return Response(serializers.UserSerializer(user).data)

    # def index(request):
    #     return HttpResponse("Thesis app")


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser or user.role == 1:
                average_score_by_school_year = Thesis.objects.values('school_year__start_year',
                                                                     'school_year__end_year').annotate(
                    avg_score=Avg('total_score'))
                major_thesis_count = Major.objects.annotate(thesis_count=Count('thesis'))

                return TemplateResponse(request, 'thesis-stats-02.html', {
                    'average_score_by_school_year': average_score_by_school_year,
                    'major_thesis_count': major_thesis_count
                })
            else:
                return HttpResponse("Tài khoản không có quyền xem thông kê")
        else:
            # Handle invalid login
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'login.html')


class LecturerCouncilsViewSet(viewsets.ViewSet, generics.ListAPIView):
    serializer_class = CouncilSerializer
    pagination_class = paginators.commonPaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        lecturer = Lecturer.objects.get(user=user)
        return Council.objects.filter(councildetail__lecturer=lecturer).distinct()
