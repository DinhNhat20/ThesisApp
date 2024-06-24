from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import EmailMessage
from django.db.models import Avg, Count
from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse
from rest_framework import viewsets, generics, status, parsers, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from etheses import settings
from theses.models import User, DepartmentAdmin, Lecturer, Student, Department, Major, SchoolYear, Position, Council, \
    CouncilDetail, Role, Thesis, ThesisScore, ScoreComponent, ScoreColumn, ScoreDetail, Supervisor, Notification, \
    NotificationUser
from theses import serializers, paginators
from theses.serializers import CouncilSerializer, StudentSerializer, Council01Serializer


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

            council = self.request.query_params.get('council')
            if council:
                queryset = queryset.filter(council=council)

        return queryset

    # Thống kê điểm trung bình của các khóa luận qua từng năm học
    @action(detail=False, methods=['get'], url_path='average-score-by-school-year')
    def average_score_by_school_year(self, request):
        # Truy vấn để tính trung bình điểm theo năm học
        average_scores = Thesis.objects.values('school_year__start_year', 'school_year__end_year') \
            .annotate(avg_score=Avg('total_score'))

        return Response(average_scores)


class Thesis01ViewSet(viewsets.ModelViewSet):
    queryset = Thesis.objects.all()
    serializer_class = serializers.Thesis01Serializer
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

            council = self.request.query_params.get('council')
            if council:
                queryset = queryset.filter(council=council)

        return queryset


class CouncilViewSet(viewsets.ModelViewSet):
    queryset = Council.objects.all()
    serializer_class = serializers.CouncilSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset

        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(name__icontains=q)

        return queryset

    # Lấy danh sách các khóa luận của 1 council
    @action(methods=['get'], url_path='theses', detail=True)
    def get_theses(self, request, pk):
        theses = self.get_object().thesis_set.filter(active=True)
        return Response(serializers.ThesisSerializer(theses, many=True).data,
                        status=status.HTTP_200_OK)


# Danh sách hội đồng có số lượng khóa luận nhỏ hơn 5
class CouncilContainThan5ThesisViewSet(viewsets.ModelViewSet):
    queryset = Council.objects.annotate(thesis_count=Count('thesis')).filter(thesis_count__lt=5)
    serializer_class = Council01Serializer
    permission_classes = [IsAuthenticated]


class DepartmentAdminViewSet(viewsets.ModelViewSet):
    queryset = DepartmentAdmin.objects.all()
    serializer_class = serializers.DepartmentAdminSerializer
    permission_classes = [IsAuthenticated]

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


class LecturerViewSet(viewsets.ModelViewSet):
    queryset = Lecturer.objects.all()
    serializer_class = serializers.LecturerSerializer
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset

        if self.action.__eq__('list'):
            q = self.request.query_params.get('q')
            if q:
                queryset = queryset.filter(full_name__icontains=q)

            code = self.request.query_params.get('code')
            if code:
                queryset = queryset.filter(code__icontains=code)

            user = self.request.query_params.get('user')
            if user:
                queryset = queryset.filter(user=user)

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


# Thống kê tần suất tham gia khóa luận của các nghành
class MajorFrequencyViewSet(viewsets.ModelViewSet):
    queryset = Major.objects.annotate(thesis_count=Count('thesis'))
    serializer_class = serializers.MajorFrequencySerializer
    http_method_names = ['get']  # Chỉ cho phép phương thức GET


class SchoolYearViewSet(viewsets.ModelViewSet):
    queryset = SchoolYear.objects.all()
    serializer_class = serializers.SchoolYearSerializer


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

    def get_queryset(self):
        queryset = super().get_queryset()

        position = self.request.query_params.get('position')
        council = self.request.query_params.get('council')

        if position and council:
            queryset = queryset.filter(position=position, council=council)

        return queryset


class CouncilDetail01Serializer(viewsets.ModelViewSet):
    queryset = CouncilDetail.objects.all()
    serializer_class = serializers.CouncilDetail01Serializer


class ThesisScoreViewSet(viewsets.ModelViewSet):
    queryset = ThesisScore.objects.all()
    serializer_class = serializers.ThesisScoreSerializer

    # Lấy danh sách các ThesisScore chứa dữ liệu được truyền vào là council_id và thesis_id
    def get_queryset(self):
        queryset = super().get_queryset()

        council_detail_id = self.request.query_params.get('council_detail')
        thesis_id = self.request.query_params.get('thesis')

        if council_detail_id and thesis_id:
            queryset = queryset.filter(council_detail_id=council_detail_id, thesis_id=thesis_id)

        return queryset


class ScoreComponentViewSet(viewsets.ModelViewSet):
    queryset = ScoreComponent.objects.all()
    serializer_class = serializers.ScoreComponentSerializer
    pagination_class = paginators.commonPaginator


class ScoreColumnViewSet(viewsets.ModelViewSet):
    queryset = ScoreColumn.objects.all()
    serializer_class = serializers.ScoreColumnSerializer


class ScoreDetailViewSet(viewsets.ModelViewSet):
    queryset = ScoreDetail.objects.all()
    serializer_class = serializers.ScoreDetailSerializer

    # Lấy danh sách ScoreDetail theo thesis_score_id
    def get_queryset(self):
        queryset = self.queryset

        if self.action.__eq__('list'):
            thesisScoreId = self.request.query_params.get('thesisScoreId')
            if thesisScoreId:
                queryset = queryset.filter(thesis_score_id=thesisScoreId)

        return queryset


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
        if self.action in ['get_current_user', 'change-password']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get', 'patch'], url_path='current-user', detail=False)
    def current_user(self, request):
        user = request.user
        if request.method.__eq__('PATCH'):
            data = request.data.copy()  # Tạo một bản sao của dữ liệu để tránh ảnh hưởng đến dữ liệu gốc
            if 'password' in data:
                data['password'] = make_password(data['password'])  # Băm mật khẩu

            serializer = serializers.UserSerializer(instance=user, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializers.UserSerializer(user).data)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser or user.role == 3:
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


# class LecturerCouncilsViewSet(viewsets.ViewSet, generics.ListAPIView):
#     serializer_class = CouncilSerializer
#     # pagination_class = paginators.commonPaginator
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         user = self.request.user
#         lecturer = Lecturer.objects.get(user=user)
#         return Council.objects.filter(councildetail__lecturer=lecturer).distinct()


class LecturerCouncilsViewSet(viewsets.ViewSet, generics.ListAPIView):
    serializer_class = CouncilSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        lecturer = Lecturer.objects.get(user=user)
        return Council.objects.filter(councildetail__lecturer=lecturer).distinct()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


# Lấy danh sách sinh viên chưa có khóa luận
class StudentsWithoutThesisView(viewsets.ModelViewSet):
    queryset = Student.objects.filter(thesis__isnull=True)
    serializer_class = StudentSerializer


# Những thay đổi
class Council01ViewSet(viewsets.ModelViewSet):
    queryset = Council.objects.all()
    serializer_class = serializers.Council01Serializer
    pagination_class = paginators.CouncilPaginator


    def get_queryset(self):
        queryset = self.queryset

        if self.action.__eq__('list'):
            q = self.request.query_params.get('q')
            if q:
                queryset = queryset.filter(name__icontains=q)

            schoolyear = self.request.query_params.get('schoolyear')
            if schoolyear:
                queryset = queryset.filter(schoolyear=schoolyear)

        return queryset

