from django.core.management.base import BaseCommand
import random

from feedback.models import Feedback
from authentication.models import User


class Command(BaseCommand):
    help = "Populate the database with sample feedback"

    def handle(self, *args, **options):
        admin_user = User.objects.filter(username="admin").first()
        if not admin_user:
            admin_user = User.objects.create_superuser(username="admin", password="adminpass", email="", role="admin")
        test_user = User.objects.filter(username="test_user").first()
        if not test_user:
            test_user = User.objects.create_user(username="test_user", password="testpass", email="", role="user")

        # Create feedback - title, description, category, status

        feedback_data = [
            {
                "title": "Login button unresponsive",
                "description": "Clicking the login button does not redirect to the dashboard. No error message is shown.",
                "category": "bug report",
                "status": "pending",
            },
            {
                "title": "Dark mode feature",
                "description": "It would be great to have a dark mode option for the interface to reduce eye strain.",
                "category": "feature request",
                "status": "pending",
            },
            {
                "title": "Spelling mistake on homepage",
                "description": "The word 'feedback' is misspelled as 'feedbak' in the homepage footer.",
                "category": "bug report",
                "status": "resolved",
            },
            {
                "title": "Add sorting feature for feedback list",
                "description": "A sorting option for feedback based on date, category, or status would be helpful.",
                "category": "feature request",
                "status": "pending",
            },
            {
                "title": "App crashes on profile update",
                "description": "Updating the user profile sometimes crashes the app. It happens mainly when changing the profile picture.",
                "category": "bug report",
                "status": "pending",
            },
            {
                "title": "Thank you for the great support!",
                "description": "The customer support team was very helpful in resolving my login issue. Keep up the good work!",
                "category": "general feedback",
                "status": "resolved",
            },
            {
                "title": "Improve mobile responsiveness",
                "description": "On smaller screens, some buttons are overlapping and the text is not aligned properly.",
                "category": "feature request",
                "status": "pending",
            },
            {
                "title": "Incorrect password reset link",
                "description": "The password reset link in the email redirects to a 404 page.",
                "category": "bug report",
                "status": "resolved",
            },
            {
                "title": "More customization options",
                "description": "Allow users to customize the dashboard layout and set preferences.",
                "category": "feature request",
                "status": "pending",
            },
            {
                "title": "Great UI design",
                "description": "I love the clean and minimalistic design of the app. It’s very user-friendly!",
                "category": "general feedback",
                "status": "resolved",
            },
        ]

        for feedback in feedback_data:
            user = random.choice([admin_user, test_user])
            Feedback.objects.create(user=user, **feedback)

        self.stdout.write(self.style.SUCCESS("Successfully populated feedback data."))
