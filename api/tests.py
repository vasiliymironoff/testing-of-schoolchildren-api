from django.test import TestCase
import rest_framework_simplejwt
from rest_framework.test import APITestCase
from rest_framework import status
from .models import CustomUser


# Созда
# ние, обновление, удаление аккаунта - AccountTest
# Exam, Statistics - ExamTest
# Comment - CommentTest


class AccountTest(APITestCase):

    def test_create_account(self):
        data = {
            "first_name": "Vasiliy",
            "last_name": "Mironov",
            "email": "v@m.com",
            "password": "123123123df",
            "is_teacher": True,
        }
        # create user
        response = self.client.post("/api/v1/auth/users/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.data
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["first_name"], "Vasiliy")
        self.assertEqual(data["last_name"], "Mironov")
        self.assertEqual(data["email"], "v@m.com")
        self.assertEqual(data["is_teacher"], True)

        # create token
        data = {
            "email": "v@m.com",
            "password": "123123123df"
        }
        response = self.client.post("/api/v1/auth/jwt/create/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data["access"]


class EditProfile(APITestCase):

    def setUp(self):
        self.first_name = "Vasiliy"
        self.last_name = "Mironov"
        self.email = "v@m.com"
        self.password = "123123123df"
        self.user = CustomUser.objects.create_user(self.email,
                                                   self.password,
                                                   first_name=self.first_name,
                                                   last_name=self.last_name,
                                                   is_teacher=True)
        refresh = rest_framework_simplejwt.tokens.RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + str(refresh.access_token))
        self.avatar = 'R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='

    def test_get_me(self):
        response = self.client.get("/api/v1/auth/users/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["first_name"], self.first_name)
        self.assertEqual(data["last_name"], self.last_name)
        self.assertEqual(data['email'], self.email)
        self.assertEqual(data["is_teacher"], True)
        self.assertEqual(data["avatar"], None)

    def test_put_users(self):
        data = {
            "last_name": "Mironov1",
        }
        response = self.client.put("/api/v1/auth/users/me/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["first_name"], self.first_name)
        self.assertEqual(data["last_name"], "Mironov1")
        self.assertEqual(data["is_teacher"], True)

    def test_update_avatar(self):
        data = {
            "avatar": self.avatar
        }
        response = self.client.put("/api/v1/profile/{}/".format(1), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertTrue(data["avatar"] is not None)

    def test_list_exam(self):
        response = self.client.get("/api/v1/exams/?page=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    def test_create_exam(self):
        data = {
            "title": "String",
            "classroom": 11,
            "subject": "al",
            "description": "Описание",
            "tasks": [
                {
                    "question": "Вопрос?",
                    "answers": [
                        {
                            "text": "text",
                            "is_correct": True
                        },
                        {
                            "text": "text",
                            "is_correct": True
                        }
                    ]
                },
                {
                    "question": "Вопрос?",
                    "answers": [
                        {
                            "text": "text",
                            "is_correct": True
                        },
                        {
                            "text": "text",
                            "is_correct": True
                        }
                    ]
                }
            ]
        }
        print(data)
        response = self.client.post("/api/v1/exams-detail/", data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["title"], "String")
        self.assertEqual(data["classroom"], 11)
        self.assertEqual(data["subject"], "al")
        self.assertEqual(data["description"], "Описание")
        tasks = data["tasks"]
        for (task, index) in enumerate(tasks):
            self.assertEqual(task["question"], "Вопрос?")
            self.assertEqual(task["id"], index+1)
            answer = task["answers"]
            self.assertEqual(answer["id"], index+1)
            self.assertEqual(answer["text"], "text")
            self.assertEqual(answer["is_correct"], True)
            self.assertEqual(task["many_option"], 1)
