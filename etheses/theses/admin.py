from django.contrib import admin
from django.utils.html import mark_safe

from theses.models import Role, User, Thesis, Council, CouncilDetail, Admin, Lecturer, Student, Faculty, Major, SchoolYear, ThesisScore, ScoreColumn, ScoreComponent, ScoreDetail, Position, Supervisor

from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


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
                    'is_active', 'date_joined', 'gender', 'phone', 'role']
    search_fields = ['id', 'username', 'first_name', 'last_name']
    list_filter = ['is_superuser', 'is_staff', 'is_active', 'role']
    readonly_fields = ['my_avatar']

    def my_avatar(self, user):
        if user.avatar:
            return mark_safe(
                f"<img src='https://res.cloudinary.com/db1p2ugkn/image/upload/v1712623700/{user.avatar}' width='150' />")


class MyThesisAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'start_date', 'complete_date', 'thesis_start_date', 'thesis_end_date', 'report_file', 'total_score', 'result', 'council', 'major', 'school_year']
    search_fields = ['id', 'name', 'code', 'total_score', 'result', 'major', 'school_year']
    list_filter = ['id', 'name', 'code', 'total_score', 'result', 'major', 'school_year']


# class MyLecturerAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name']
#     search_fields = ['id', 'name']
#     list_filter = ['id', 'name']


admin.site.register(Role, MyRoleAdmin)
admin.site.register(User, MyUserAdmin)
admin.site.register(Thesis, MyThesisAdmin)
admin.site.register(Admin)
admin.site.register(Lecturer)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Major)
admin.site.register(SchoolYear)
admin.site.register(ThesisScore)
admin.site.register(ScoreColumn)
admin.site.register(ScoreComponent)
admin.site.register(ScoreDetail)
admin.site.register(Position)
admin.site.register(Council)
admin.site.register(CouncilDetail)
admin.site.register(Supervisor)



