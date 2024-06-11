from django.contrib import admin
from django.db.models import Count, Avg
from django.template.response import TemplateResponse
from django.utils.html import mark_safe

from theses.models import Role, User, Thesis, Council, CouncilDetail, DepartmentAdmin, Lecturer, Student, Department, \
    Major, SchoolYear, ThesisScore, ScoreColumn, ScoreComponent, ScoreDetail, Position, Supervisor, Notification, \
    NotificationUser

from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.urls import path


class RoleForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Role
        fields = '__all__'


class MyRoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['id', 'name']
    list_filter = ['id', 'name']


class MyUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'password', 'is_superuser', 'first_name', 'last_name', 'email', 'is_staff',
                    'is_active', 'date_joined', 'role']
    search_fields = ['id', 'username', 'first_name', 'last_name']
    list_filter = ['is_superuser', 'is_staff', 'is_active', 'role']
    readonly_fields = ['my_avatar']

    def my_avatar(self, user):
        if user.avatar:
            return mark_safe(
                f"<img src='https://res.cloudinary.com/db1p2ugkn/image/upload/v1712623700/{user.avatar}' width='150' />")


class MyThesisAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'start_date', 'complete_date', 'report_file', 'total_score', 'result',
                    'council', 'major', 'school_year']
    search_fields = ['id', 'name', 'code', 'total_score', 'result', 'major', 'school_year']
    list_filter = ['id', 'name', 'code', 'total_score', 'result', 'major', 'school_year']


class MyLecturerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['id', 'name']
    list_filter = ['id', 'name']


class ThesisAppAdminSite(admin.AdminSite):
    site_header = 'HỆ THỐNG QUẢN LÝ KHÓA LUẬN TỐT NGHIỆP'

    def get_urls(self):
        return [
            path('thesis-stats/', self.thesis_stats)
        ] + super().get_urls()

    def thesis_stats(self, request):
        average_score_by_school_year = Thesis.objects.values('school_year__start_year', 'school_year__end_year').annotate(avg_score=Avg('total_score'))
        major_thesis_count = Major.objects.annotate(thesis_count=Count('thesis'))

        return TemplateResponse(request, 'admin/thesis-stats.html', {
            'average_score_by_school_year': average_score_by_school_year,
            'major_thesis_count': major_thesis_count
        })


admin_site = ThesisAppAdminSite('mythesis')

# admin.site.register(Role, MyRoleAdmin)
# admin.site.register(User, MyUserAdmin)
# admin.site.register(Thesis, MyThesisAdmin)
# admin.site.register(DepartmentAdmin)
# admin.site.register(Lecturer)
# admin.site.register(Student)
# admin.site.register(Department)
# admin.site.register(Major)
# admin.site.register(SchoolYear)
# admin.site.register(ThesisScore)
# admin.site.register(ScoreColumn)
# admin.site.register(ScoreComponent)
# admin.site.register(ScoreDetail)
# admin.site.register(Position)
# admin.site.register(Council)
# admin.site.register(CouncilDetail)
# admin.site.register(Supervisor)
# admin.site.register(Notification)
# admin.site.register(NotificationUser)

admin_site.register(Role, MyRoleAdmin)
admin_site.register(User, MyUserAdmin)
admin_site.register(Thesis, MyThesisAdmin)
admin_site.register(DepartmentAdmin)
admin_site.register(Lecturer)
admin_site.register(Student)
admin_site.register(Department)
admin_site.register(Major)
admin_site.register(SchoolYear)
admin_site.register(ThesisScore)
admin_site.register(ScoreColumn)
admin_site.register(ScoreComponent)
admin_site.register(ScoreDetail)
admin_site.register(Position)
admin_site.register(Council)
admin_site.register(CouncilDetail)
admin_site.register(Supervisor)
admin_site.register(Notification)
admin_site.register(NotificationUser)
