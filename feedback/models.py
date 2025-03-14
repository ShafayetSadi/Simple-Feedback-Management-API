from django.conf import settings
from django.db import models


class Feedback(models.Model):
    CATEGORY_CHOICES = [
        ("bug_report", "Bug Report"),
        ("feature_request", "Feature Request"),
        ("general_feedback", "General Feedback"),
    ]
    STATUS_CHOICES = [("pending", "Pending"), ("resolved", "Resolved")]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="feedbacks")
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + " - " + self.user.username
