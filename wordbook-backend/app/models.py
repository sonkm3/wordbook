from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

from django.dispatch import receiver

from djoser.signals import user_registered


class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError("The email must be set")
        email = self.normalize_email(email)

        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField("username", max_length=150, blank=True, null=True)
    email = models.EmailField("email address", unique=True)

    # We can remove inherited fields with setting them to None if it inherited from Abstract Class.
    # https://docs.djangoproject.com/en/dev/topics/db/models/#field-name-hiding-is-not-permitted
    first_name = None
    last_name = None

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class WordManager(models.Manager):
    def student(self, student):
        return super().get_queryset().filter(course__student=student).order_by("id")

    def course(self, student, course):
        return (
            super()
            .get_queryset()
            .filter(course__student=student, course=course)
            .order_by("id")
        )


class Word(models.Model):
    word = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    pronunciation = models.TextField(null=True, blank=True)
    hint = models.TextField(null=True, blank=True)
    image_hint = models.ImageField(upload_to="hint_images", null=True, blank=True)
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.word

    objects = WordManager()


class CourseManager(models.Manager):
    def student(self, student):
        return super().get_queryset().filter(student=student).order_by("id")


class Course(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    objects = CourseManager()


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} {self.user.email}"


@receiver(user_registered)
def create_student(sender, **kwargs):
    Student.objects.create(user=kwargs["user"])
