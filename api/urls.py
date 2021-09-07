from rest_framework.routers import DefaultRouter
from . import views
from django.conf.urls import url
from django.urls import include

urlpatterns = [
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.jwt')),
]

router = DefaultRouter()
router.register('exam', views.ExamViewSet)
router.register('exam-detail', views.ExamWithTaskViewSet)

urlpatterns += router.urls

