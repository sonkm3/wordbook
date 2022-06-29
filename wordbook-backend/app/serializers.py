from rest_framework import serializers

from .models import Word, Course


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = "__all__"
        read_only_fields = ('created_at', 'updated_at')

    def validate_course(self, course):
        if self.context["request"].user != course.student.user:
            message = "Owner and request user must be matched."
            raise serializers.ValidationError(message)
        return course

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        if hasattr(data, "course_pk"):
            ret["course"] = data.pop("course_pk")
        return ret


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ('created_at', 'updated_at')

    def validate_student(self, student):
        if self.context["request"].user != student.user:
            message = "Owner and request user must be matched."
            raise serializers.ValidationError(message)
        return student

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        if hasattr(data, "student"):
            data.pop("student")
        ret["student"] = self.context["request"].user.student
        return ret
