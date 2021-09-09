from rest_framework import viewsets
from .models import Exam, Statistics, Profile, Comment
from rest_framework import mixins
from .permissions import IsTeacherUser
from . import serializers


class ExamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Exam.objects.filter(is_show=True)

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.ExamListSerializer
        else:
            return serializers.ExamRetrieveSerializer


class ExamWithTaskViewSet(viewsets.GenericViewSet,
                          mixins.RetrieveModelMixin,
                          mixins.CreateModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin):
    permission_classes = [IsTeacherUser, ]
    serializer_class = serializers.ExamSerializer

    def get_queryset(self):
        if self.action == "retrieve":
            return Exam.objects.all()
        else:
            return Exam.objects.all()


class CommentViewSet(viewsets.GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin):
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)


class StatisticsViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin):
    serializer_class = serializers.StatisticsSerializer

    def get_queryset(self):
        return Statistics.objects.filter(user=self.request.user)


class ProfileViewSet(viewsets.GenericViewSet,
                     mixins.UpdateModelMixin):
    serializer_class = serializers.ProfileSerializer
    queryset = Profile.objects.all()

