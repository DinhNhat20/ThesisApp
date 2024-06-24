from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import routers
from theses import views
from .admin import admin_site

r = routers.DefaultRouter()
r.register('roles', views.RoleViewSet, 'roles')
r.register('theses', views.ThesisViewSet, 'theses')
r.register('councils', views.CouncilViewSet, 'councils')
r.register('lecturers', views.LecturerViewSet, 'lecturers')
r.register('students', views.StudentViewSet, 'students')
r.register('departments', views.DepartmentViewSet, 'departments')
r.register('majors', views.MajorViewSet, 'majors')
r.register('school_years', views.SchoolYearViewSet, 'school_years')
r.register('positions', views.PositionViewSet, 'positions')
r.register('supervisors', views.SupervisorViewSet, 'supervisors')
r.register('department_admins', views.DepartmentAdminViewSet, 'department_admin')
r.register('council_details', views.CouncilDetailViewSet, 'council_detail')
r.register('score_columns', views.ScoreColumnViewSet, 'score_column')
r.register('sore_components', views.ScoreComponentViewSet, 'sore_component')
r.register('thesis_scores', views.ThesisScoreViewSet, 'thesis_score')
r.register('score_details', views.ScoreDetailViewSet, 'score_detail')
r.register('notifications', views.NotificationViewSet, 'notification')
r.register('notification_users', views.NotificationUserViewSet, 'notification_user')
r.register('users', views.UserViewSet, 'users')
r.register('lecturer-councils', views.LecturerCouncilsViewSet, 'lecturer-councils')
r.register('students-without-thesis', views.StudentsWithoutThesisView, 'students-without-thesis')
r.register('theses01', views.Thesis01ViewSet, 'theses01'),
r.register('councils-contain-than-5-thesis', views.CouncilContainThan5ThesisViewSet, 'councils-contain-than-5-thesis')
r.register('create_council_detail', views.CouncilDetail01Serializer, 'create_council_detail'),
r.register('councils01', views.Council01ViewSet, 'councils01'),
r.register('major_frequency', views.MajorFrequencyViewSet, 'major_frequency'),

urlpatterns = [
    path('', include(r.urls)),
    path('admin/', admin_site.urls),
    path('login/', views.user_login, name='login'),
]
