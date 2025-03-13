from django.urls import path

from . import views

urlpatterns = [
    path("feedback/", views.FeedbackAPIView.as_view()),
    path("feedback/<int:pk>/", views.FeedbackDetailAPIView.as_view()),
]
