import json
from django.test import TestCase

# from django.contrib.auth.models import User
from rest_framework.test import APIClient

from app.models import Word, Course, Student
from app.models import CustomUser


class WordModelTestCase(TestCase):
    def setUp(self):
        pass

    def test_model_relation(self):
        user = CustomUser.objects.create_user(
            "example", "example@example.com", "example"
        )
        student = Student.objects.create(user=user)
        course = Course.objects.create(title="title", student=student)
        word = Word.objects.create(word="test", course=course)

    def test_word_manager(self):
        user1 = CustomUser.objects.create_user(
            "example1", "example1@example.com", "example"
        )
        user2 = CustomUser.objects.create_user(
            "example2", "example2@example.com", "example"
        )
        student1 = Student.objects.create(user=user1)
        student2 = Student.objects.create(user=user2)
        course1 = Course.objects.create(title="title", student=student1)
        course2 = Course.objects.create(title="title", student=student2)
        word = Word.objects.create(word="test", course=course1)

        self.assertEqual(word, Word.objects.student(student1)[0])
        self.assertListEqual([], list(Word.objects.student(student2)))

        self.assertEqual(word, Word.objects.course(student1, course1)[0])
        self.assertListEqual([], list(Word.objects.course(student1, course2)))


class AccountViewTest(TestCase):
    def test_create_user_and_student(self):
        client = APIClient()
        response = client.post(
            "http://testserver/auth/users/",
            {"email": "djoser@example.com", "password": "alpine12"},
        )
        self.assertEqual(1, Student.objects.all().count())
        self.assertEqual(1, CustomUser.objects.all().count())


class WordViewTestCase(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            "example1", "example1@example.com", "example"
        )
        self.user2 = CustomUser.objects.create_user(
            "example2", "example2@example.com", "example"
        )
        self.student1 = Student.objects.create(user=self.user1)
        self.student2 = Student.objects.create(user=self.user2)
        self.course1 = Course.objects.create(title="title", student=self.student1)
        self.course2 = Course.objects.create(title="title", student=self.student2)
        self.word = Word.objects.create(word="test", course=self.course1)

    def test_get_words_success(self):
        client = APIClient()
        client.force_authenticate(user=self.student1.user)
        response = client.get(f"http://testserver/courses/{self.course1.id}/words/")
        self.assertEqual(
            self.word.word, json.loads(response.content)["data"][0]["word"]
        )
        self.assertEqual(self.word, Word.objects.student(self.student1)[0])

    def test_get_word_success(self):
        client = APIClient()
        client.force_authenticate(user=self.student1.user)
        response = client.get(
            f"http://testserver/courses/{self.course1.id}/words/{self.word.id}/"
        )
        self.assertEqual(self.word.word, json.loads(response.content)["word"])

    def test_post_word_success(self):
        client = APIClient()
        client.force_authenticate(user=self.student1.user)
        response = client.post(
            # f"http://testserver/courses/{self.course1.id}/words/", {"word": "new", "course": self.course1.id}
            f"http://testserver/courses/{self.course1.id}/words/",
            {"word": "new"},
        )
        self.assertEqual(201, response.status_code)
        self.assertEqual(2, Word.objects.all().count())

    def test_patch_word_success(self):
        client = APIClient()
        client.force_authenticate(user=self.student1.user)
        response = client.patch(
            f"http://testserver/courses/{self.course1.id}/words/{self.word.id}/",
            {"word": "update"},
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual("update", Word.objects.all()[0].word)

    def test_delete_word_success(self):
        client = APIClient()
        client.force_authenticate(user=self.student1.user)
        response = client.delete(
            f"http://testserver/courses/{self.course1.id}/words/{self.word.id}/"
        )
        self.assertEqual(204, response.status_code)

    def test_get_word_fail(self):
        client = APIClient()
        client.force_authenticate(user=self.student2.user)
        response = client.get(
            f"http://testserver/courses/{self.course1.id}/words/{self.word.id}/"
        )
        self.assertEqual(404, response.status_code)

    def test_post_word_fail(self):
        client = APIClient()
        client.force_authenticate(user=self.student2.user)
        response = client.post(
            f"http://testserver/courses/{self.course1.id}/words/", {"word": "new"}
        )
        self.assertEqual(400, response.status_code)

    def test_patch_word_fail(self):
        client = APIClient()
        client.force_authenticate(user=self.student2.user)
        response = client.patch(
            f"http://testserver/courses/{self.course1.id}/words/{self.word.id}/",
            {"word": "update"},
        )
        self.assertEqual(404, response.status_code)

    def test_delete_word_fail(self):
        client = APIClient()
        client.force_authenticate(user=self.student2.user)
        response = client.delete(
            f"http://testserver/courses/{self.course1.id}/words/{self.word.id}/"
        )
        self.assertEqual(404, response.status_code)


class CourseViewTestCase(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            "example1", "example1@example.com", "example"
        )
        self.user2 = CustomUser.objects.create_user(
            "example2", "example2@example.com", "example"
        )
        self.student1 = Student.objects.create(user=self.user1)
        self.student2 = Student.objects.create(user=self.user2)
        self.course1 = Course.objects.create(title="title", student=self.student1)
        self.course2 = Course.objects.create(title="title", student=self.student1)
        self.course3 = Course.objects.create(title="title", student=self.student2)
        self.word = Word.objects.create(word="test", course=self.course1)

    def test_get_courses_success(self):
        client = APIClient()
        client.force_authenticate(user=self.student1.user)
        response = client.get("http://testserver/courses/")
        self.assertEqual(
            self.course1.title, json.loads(response.content)["data"][0]["title"]
        )
        self.assertEqual(self.word, Word.objects.student(self.student1)[0])
        self.assertEqual(2, len(json.loads(response.content)))

    def test_get_course_success(self):
        client = APIClient()
        client.force_authenticate(user=self.student1.user)
        response = client.get(f"http://testserver/courses/{self.course1.id}/")
        self.assertEqual(self.course1.title, json.loads(response.content)["title"])

    def test_post_course_success(self):
        client = APIClient()
        client.force_authenticate(user=self.student1.user)
        response = client.post(
            "http://testserver/courses/", {"title": "new", "student": self.student1.id}
        )
        self.assertEqual(201, response.status_code)
        self.assertEqual(4, Course.objects.all().count())

    def test_patch_course_success(self):
        client = APIClient()
        client.force_authenticate(user=self.student1.user)
        response = client.patch(
            f"http://testserver/courses/{self.course1.id}/",
            {"title": "update"},
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual("update", Course.objects.all()[0].title)

    def test_delete_course_success(self):
        client = APIClient()
        client.force_authenticate(user=self.student1.user)
        response = client.delete(f"http://testserver/courses/{self.course1.id}/")
        self.assertEqual(204, response.status_code)

    def test_get_course_fail(self):
        client = APIClient()
        client.force_authenticate(user=self.student2.user)
        response = client.get(f"http://testserver/courses/{self.course1.id}/")
        self.assertEqual(404, response.status_code)

    def test_post_course_fail(self):
        client = APIClient()
        client.force_authenticate(user=self.student2.user)
        response = client.post(
            "http://testserver/courses/", {"title": "new", "student": self.student1.id}
        )
        self.assertEqual(400, response.status_code)

    def test_patch_course_fail(self):
        client = APIClient()
        client.force_authenticate(user=self.student2.user)
        response = client.patch(
            f"http://testserver/courses/{self.course1.id}/",
            {"title": "update"},
        )
        self.assertEqual(404, response.status_code)

    def test_delete_course_fail(self):
        client = APIClient()
        client.force_authenticate(user=self.student2.user)
        response = client.delete(f"http://testserver/courses/{self.course1.id}/")
        self.assertEqual(404, response.status_code)
