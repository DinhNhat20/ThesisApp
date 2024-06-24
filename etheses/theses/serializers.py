from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from theses.models import User, DepartmentAdmin, Lecturer, Student, Department, Major, SchoolYear, Position, Council, \
    CouncilDetail, Role, Thesis, ThesisScore, ScoreComponent, ScoreColumn, ScoreDetail, Supervisor, Notification, \
    NotificationUser
from theses.utils import send_reviewer_email


class ItemSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['image'] = instance.image.url

        return rep


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = ['id', 'code', 'name', 'department']


class MajorSerializer01(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = ['name']


class MajorFrequencySerializer(serializers.ModelSerializer):
    thesis_count = serializers.IntegerField()

    class Meta:
        model = Major
        fields = ['id', 'name', 'thesis_count']


class SchoolYearSerializer01(serializers.ModelSerializer):
    class Meta:
        model = SchoolYear
        fields = ['start_year', 'end_year']


class ThesisSerializer(serializers.ModelSerializer):
    major = MajorSerializer01(read_only=True)
    school_year = SchoolYearSerializer01(read_only=True)

    average_score = serializers.SerializerMethodField()

    # Tính điểm trung bình của khóa luận
    def get_average_score(self, obj):
        return obj.average_score()

    class Meta:
        model = Thesis
        fields = ['id', 'code', 'name', 'start_date', 'complete_date', 'average_score', 'result', 'major',
                  'school_year', 'council', 'lecturers', 'created_date', 'report_file', 'reviewer']


class Thesis01Serializer(serializers.ModelSerializer):
    class Meta:
        model = Thesis
        fields = ['id', 'code', 'name', 'start_date', 'complete_date', 'major', 'school_year', 'council', 'reviewer',
                  'created_date']


class CouncilSerializer(serializers.ModelSerializer):
    # Phương thức để lấy dữ liệu mở rộng (chi tiết)
    details = serializers.SerializerMethodField()

    class Meta:
        model = Council
        fields = ['id', 'name', 'description', 'created_date', 'schoolyear', 'active', 'details']

    # Lấy chi tiết các trường dữ liệu của CouncilDetail thuộc hội đồng của 1 giảng viên cụ thể
    def get_details(self, obj):
        request = self.context.get('request')
        lecturer = Lecturer.objects.get(user=request.user)
        details = CouncilDetail.objects.filter(council=obj, lecturer=lecturer)
        return CouncilDetailSerializer(details, many=True).data


class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class DepartmentAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentAdmin
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class SchoolYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolYear
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['name']


class SupervisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supervisor
        fields = '__all__'


class CouncilDetailSerializer(serializers.ModelSerializer):
    # Lấy dữ liệu name thay cho id của khóa ngoại position
    position = serializers.CharField(source='position.name')

    class Meta:
        model = CouncilDetail
        fields = ['id', 'position', 'lecturer', 'council']


class CouncilDetail01Serializer(serializers.ModelSerializer):
    position = serializers.PrimaryKeyRelatedField(queryset=Position.objects.all())
    lecturer = serializers.PrimaryKeyRelatedField(queryset=Lecturer.objects.all())
    council = serializers.PrimaryKeyRelatedField(queryset=Council.objects.all())

    class Meta:
        model = CouncilDetail
        fields = ['id', 'position', 'lecturer', 'council']

    def create(self, validated_data):
        # Dữ liệu đã được xác thực từ phía client
        position = validated_data.get('position')
        lecturer = validated_data.get('lecturer')
        council = validated_data.get('council')

        # Tạo đối tượng
        council_detail = CouncilDetail.objects.create(
            position=position,
            lecturer=lecturer,
            council=council
        )

        # Gửi email nếu position là 3 (Phản biện)
        if position == 3:
            try:
                lecturer = Lecturer.objects.filter(id=lecturer)
                lecturer_email = lecturer.user.email
                send_reviewer_email(lecturer_email, council)
            except Exception as e:
                raise ValidationError(f"Failed to send email to {lecturer.full_name}: {str(e)}")

        return council_detail


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class ScoreComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreComponent
        fields = '__all__'


class ScoreColumnSerializer(serializers.ModelSerializer):
    # Lấy dữ liệu name thay cho id của khóa ngoại ScoreComponent
    score_component = serializers.CharField(source='score_component.name', read_only=True)

    class Meta:
        model = ScoreColumn
        fields = ['id', 'name', 'weight', 'score_component']


class ThesisScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThesisScore
        fields = '__all__'


class ScoreDetailSerializer(serializers.ModelSerializer):
    score_component_name = serializers.SerializerMethodField()

    class Meta:
        model = ScoreDetail
        fields = ['id', 'created_date', 'updated_date', 'active', 'score', 'thesis_score', 'score_column',
                  'score_component_name']

    # Lấy name của Score Component thông qua khóa ngoại Score Column của Score Detail
    def get_score_component_name(self, obj):
        return obj.score_column.score_component.name


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class NotificationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationUser
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['avatar'] = instance.avatar.url

        return rep

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(user.password)
        user.save()

        return user

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'avatar', 'role']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class Council01Serializer(serializers.ModelSerializer):
    class Meta:
        model = Council
        fields = '__all__'


