from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import routers
from theses import views

r = routers.DefaultRouter()
r.register('roles', views.RoleViewSet, 'roles')
r.register('theses', views.ThesisViewSet, 'theses')
r.register('councils', views.CouncilViewSet, 'councils')
r.register('lecturers', views.LecturerViewSet, 'lecturers')
r.register('students', views.StudentViewSet, 'students')
r.register('faculties', views.FacultyViewSet, 'faculties')
r.register('majors', views.MajorViewSet, 'majors')
r.register('schoolyears', views.SchoolYearViewSet, 'schoolyears')
r.register('positions', views.PositionViewSet, 'positions')
r.register('supervisors', views.SupervisorViewSet, 'supervisors')
r.register('users', views.UserViewSet, 'users')

urlpatterns = [
    path('', include(r.urls))
]