from rest_framework.routers import DefaultRouter
from . import views
from django.conf.urls import url
from django.urls import path, include

urlpatterns = [
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
]

router = DefaultRouter()
router.register('exams', views.ExamViewSet)
router.register('exams-detail', views.ExamWithTaskViewSet, basename="Exam")
router.register("exams-me", views.ExamsMeViewSet, basename="Exam")
router.register("exams-statistics", views.ExamsStatisticsViewSet, basename="Exam")
router.register("statistics", views.StatisticsViewSet, basename="Statistics")
router.register("comments", views.CommentViewSet, basename="Comment")
router.register("profiles", views.ProfileViewSet, basename="Profile")
router.register("tasks", views.TaskViewSet, basename="Task")
router.register("answers", views.AnswerViewSet, basename="Answer")

urlpatterns += router.urls

