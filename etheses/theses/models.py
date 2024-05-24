from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Role(models.Model):
    name = models.CharField(max_length=20, null=False)

    def __str__(self):
        return self.name


class User(AbstractUser):
    avatar = CloudinaryField(null=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True)
    notifications = models.ManyToManyField('Notification', through='NotificationUser', null=True, blank=True)


class DepartmentAdmin(models.Model):
    code = models.CharField(max_length=10, null=False)
    full_name = models.CharField(max_length=50, null=False)
    gender = models.CharField(max_length=15, null=False)
    phone = models.CharField(max_length=10, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.full_name


class SchoolYear(models.Model):
    start_year = models.DateField()
    end_year = models.DateField()

    def __str__(self):
        return f"{self.start_year} - {self.end_year}"


class Department(models.Model):
    code = models.CharField(max_length=10, null=False)
    name = models.CharField(max_length=80, null=False)

    def __str__(self):
        return self.name


class Major(models.Model):
    code = models.CharField(max_length=10, null=False)
    name = models.CharField(max_length=80, null=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Council(BaseModel):
    name = models.CharField(max_length=50, null=False)
    description = RichTextField(null=True, blank=True)
    schoolyear = models.ForeignKey(SchoolYear, on_delete=models.PROTECT)
    lecturers = models.ManyToManyField('Lecturer', through='CouncilDetail', null=True, blank=True)

    def __str__(self):
        return self.name


class Lecturer(models.Model):
    code = models.CharField(max_length=10, null=False)
    full_name = models.CharField(max_length=50, null=False)
    birthday = models.DateField(null=False)
    gender = models.CharField(max_length=15, null=False)
    phone = models.CharField(max_length=10, null=False)
    address = models.CharField(max_length=100, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name


class Position(models.Model):
    name = models.CharField(max_length=15, null=False)

    def __str__(self):
        return self.name


class CouncilDetail(models.Model):
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    council = models.ForeignKey(Council, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.PROTECT)
    theses = models.ManyToManyField('thesis', through='ThesisScore', null=True, blank=True)

    def __str__(self):
        return f"{self.lecturer}"


class Thesis(BaseModel):
    code = models.CharField(max_length=10, null=False)
    name = models.CharField(max_length=200, null=False)
    start_date = models.DateField()
    complete_date = models.DateField()
    report_file = RichTextField(null=True, blank=True)
    total_score = models.FloatField(null=True, default=0)
    result = models.BooleanField(default=False)
    major = models.ForeignKey(Major, on_delete=models.PROTECT)
    school_year = models.ForeignKey(SchoolYear, on_delete=models.PROTECT)
    council = models.ForeignKey(Council, on_delete=models.PROTECT)
    lecturers = models.ManyToManyField('Lecturer', through='Supervisor', null=True, blank=True)

    def __str__(self):
        return self.code


class Supervisor(models.Model):
    lecturer = models.ForeignKey(Lecturer, on_delete=models.PROTECT)
    thesis = models.ForeignKey(Thesis, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.lecturer} hướng dẫn {self.thesis}"


class Student(models.Model):
    code = models.CharField(max_length=10, null=False)
    full_name = models.CharField(max_length=50, null=False)
    birthday = models.DateField(null=False)
    gender = models.CharField(max_length=15, null=False)
    phone = models.CharField(max_length=10, null=False)
    address = models.CharField(max_length=100, null=False)
    gpa = models.FloatField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    major = models.ForeignKey(Major, on_delete=models.PROTECT)
    thesis = models.ForeignKey(Thesis, on_delete=models.PROTECT)

    def __str__(self):
        return self.full_name


class ScoreComponent(models.Model):
    name = models.CharField(max_length=20, null=False)
    evalution_method = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.name


class ScoreColumn(models.Model):
    name = models.CharField(max_length=20, null=False)
    weight = models.FloatField(null=False)
    score_component = models.ForeignKey(ScoreComponent, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class ThesisScore(models.Model):
    council_detail = models.ForeignKey(CouncilDetail, on_delete=models.PROTECT)
    thesis = models.ForeignKey(Thesis, on_delete=models.CASCADE)
    scoreColumns = models.ManyToManyField('ScoreColumn', through='ScoreDetail', null=True, blank=True)

    def __str__(self):
        return f"{self.council_detail} - {self.thesis}"


class ScoreDetail(models.Model):
    score = models.FloatField()
    thesis_score = models.ForeignKey(ThesisScore, on_delete=models.CASCADE)
    score_column = models.ForeignKey(ScoreColumn, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.thesis_score} - {self.score_column}"


class Notification(BaseModel):
    title = models.CharField(max_length=150, null=False)
    content = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.title


class NotificationUser(models.Model):
    active = models.BooleanField(default=True)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.notification} - {self.user}"
