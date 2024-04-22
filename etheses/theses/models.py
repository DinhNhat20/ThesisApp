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
    gender = models.CharField(max_length=15, null=False)
    phone = models.CharField(max_length=10, null=False)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True)


class Admin(models.Model):
    full_name = models.CharField(max_length=50, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.full_name


class SchoolYear(models.Model):
    start_year = models.DateField()
    end_year = models.DateField()



class Faculty(models.Model):
    code = models.CharField(max_length=10, null=False)
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name


class Major(models.Model):
    code = models.CharField(max_length=10, null=False)
    name = models.CharField(max_length=50, null=False)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Council(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = RichTextField()
    is_block = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    # lecturers = models.ManyToManyField(Lecturer, null=True, blank=True)

    def __str__(self):
        return self.name


class Lecturer(models.Model):
    code = models.CharField(max_length=10, null=False)
    full_name = models.CharField(max_length=50, null=False)
    birthday = models.DateField(null=False)
    address = models.CharField(max_length=100, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.code


class Position(models.Model):
    name = models.CharField(max_length=15, null=False)

    def __str__(self):
        return self.name


class CouncilDetail(models.Model):
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    council = models.ForeignKey(Council, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.PROTECT)


class Thesis(models.Model):
    code = models.CharField(max_length=10, null=False)
    name = models.CharField(max_length=200, null=False)
    start_date = models.DateField()
    complete_date = models.DateField()
    thesis_start_date = models.DateField()
    thesis_end_date = models.DateField()
    report_file = RichTextField()
    total_score = models.FloatField(null=True, default=0)
    result = models.BooleanField(default=False)
    major = models.ForeignKey(Major, on_delete=models.PROTECT)
    school_year = models.ForeignKey(SchoolYear, on_delete=models.PROTECT)
    council = models.ForeignKey(Council, on_delete=models.PROTECT)
    # lecturers = models.ManyToManyField(Lecturer, null=True, blank=True)

    def __str__(self):
        return self.code


class Supervisor(models.Model):
    lecturer = models.ForeignKey(Lecturer, on_delete=models.PROTECT)
    thesis = models.ForeignKey(Thesis, on_delete=models.PROTECT)


class Student(models.Model):
    code = models.CharField(max_length=10, null=False)
    full_name = models.CharField(max_length=50, null=False)
    birthday = models.DateField(null=False)
    address = models.CharField(max_length=100, null=False)
    gpa = models.FloatField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    major = models.ForeignKey(Major, on_delete=models.PROTECT)
    thesis = models.ForeignKey(Thesis, on_delete=models.PROTECT)

    def __str__(self):
        return self.code


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


class ScoreDetail(models.Model):
    score = models.FloatField()
    thesis_score = models.ForeignKey(ThesisScore, on_delete=models.CASCADE)
    score_column = models.ForeignKey(ScoreColumn, on_delete=models.CASCADE)
