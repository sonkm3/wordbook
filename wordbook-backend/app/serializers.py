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
