__author__ = 'sweemeng'
from rest_framework.test import APITestCase
from rest_framework import status
from popit.models import Post
from rest_framework.authtoken.models import Token


class PostAPITestCase(APITestCase):

    fixtures = [ "api_request_test_data.yaml" ]

    def test_view_post_list(self):

        response = self.client.get("/en/posts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_post_detail_not_exist_unauthorized(self):
        response = self.client.get("/en/posts/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_view_post_detail_not_exist_authorized(self):
        response = self.client.get("/en/posts/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_view_post_detail_exist_unauthorized(self):
        response = self.client.get("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_post_detail_exist_authorized(self):
        response = self.client.get("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post_unauthorized(self):
        data = {
            "label": "Honorary Member",
            "organization_id": "3d62d9ea-0600-4f29-8ce6-f7720fd49aa3",
            "role": "Honorary Member",
            "area_id": "640c0f1d-2305-4d17-97fe-6aa59f079cc4",
            "start_date": "2000-2-2",
            "end_date": "2030-2-2",
        }
        response = self.client.post("/en/posts/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_authorized(self):
        data = {
            "label": "Honorary Member",
            "organization_id": "3d62d9ea-0600-4f29-8ce6-f7720fd49aa3",
            "role": "Honorary Member",
            "area_id": "640c0f1d-2305-4d17-97fe-6aa59f079cc4",
            "start_date": "2000-2-2",
            "end_date": "2030-2-2",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post("/en/posts/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post = Post.objects.language("en").get(role="Honorary Member")
        self.assertEqual(post.organization_id, "3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")

    def test_update_post_unauthorized(self):
        data = {
            "label": "member"
        }
        response = self.client.put("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_not_exist_unauthorized(self):
        data = {
            "label": "member"
        }
        response = self.client.put("/en/posts/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_authorized(self):
        data = {
            "label": "member"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        self.assertEqual(post.label, "member")

    def test_update_post_not_exist_authorized(self):
        data = {
            "label": "member"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/posts/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_post_unauthorized(self):
        response = self.client.delete("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_post_not_exist_unauthorized(self):
        response = self.client.delete("/en/posts/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_post_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.delete("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_post_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.delete("/en/posts/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
