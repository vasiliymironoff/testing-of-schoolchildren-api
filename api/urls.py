from rest_framework.routers import DefaultRouter
from . import views
from django.conf.urls import url
from django.urls import path, include

urlpatterns = [
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.jwt')),
]

router = DefaultRouter()
router.register('exams', views.ExamViewSet)
router.register('exams-detail', views.ExamWithTaskViewSet, basename="Exam")
router.register("statistics", views.StatisticsViewSet, basename="Statistics")
router.register("comment", views.CommentViewSet, basename="Comment")
router.register("profile", views.ProfileViewSet, basename="Profile")
urlpatterns += router.urls

