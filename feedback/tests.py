from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from authentication.models import User
from feedback.models import Feedback


class FeedbackTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.admin = User.objects.create_user(username="admin", password="adminpassword", role="admin")

        self.feedback_data = {
            "title": "Bug in login",
            "description": "Login button not working",
            "category": "bug_report",
            "status": "pending",
        }
        self.update_data = {
            "title": "Updated bug title",
            "description": "Fixed issue",
            "category": "bug_report",
            "status": "resolved",
        }

        self.user_token = str(AccessToken.for_user(self.user))
        self.admin_token = str(AccessToken.for_user(self.admin))

    def test_create_feedback_authenticated(self):
        """Test that an authenticated user can create feedback."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.post("/api/feedback/", self.feedback_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get("title"), "Bug in login")

    def test_create_feedback_unauthenticated(self):
        """Test that an unauthenticated user cannot create feedback."""
        response = self.client.post("/api/feedback/", self.feedback_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json().get("detail"), "Authentication credentials were not provided.")

    def test_retrieve_feedback_by_admin(self):
        """Test that an admin can retrieve all feedback."""
        Feedback.objects.create(user=self.user, **self.feedback_data)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.get("/api/feedback/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_single_feedback(self):
        """Test that a user can retrieve a single feedback."""
        feedback = Feedback.objects.create(user=self.user, **self.feedback_data)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.get(f"/api/feedback/{feedback.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("id"), 1)

    def test_update_feedback_by_owner(self):
        """Test that a user can update their own feedback."""
        feedback = Feedback.objects.create(user=self.user, **self.feedback_data)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.put(f"/api/feedback/{feedback.id}/", self.update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_feedback_by_non_owner(self):
        """Test that a user cannot update another user's feedback."""
        other_user = User.objects.create_user(username="otheruser", password="password123")
        feedback = Feedback.objects.create(user=other_user, **self.feedback_data)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.put(f"/api/feedback/{feedback.id}/", self.update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json().get("detail"), "You do not have permission to perform this action.")

    def test_delete_feedback_by_admin(self):
        """Test that an admin can delete any feedback."""
        feedback = Feedback.objects.create(user=self.user, **self.feedback_data)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.delete(f"/api/feedback/{feedback.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_feedback_invalid_data(self):
        """Test that creating feedback with invalid data returns a 400 error."""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.post("/api/feedback/", {"title": "", "description": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_feedback_invalid_status(self):
        """Test that updating feedback with an invalid status returns a 400 error."""
        feedback = Feedback.objects.create(user=self.user, **self.feedback_data)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.put(f"/api/feedback/{feedback.id}/", {"status": "invalid_status"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
