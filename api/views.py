from rest_framework import viewsets
from .models import Exam, Statistics, Profile, Comment, Task, Answer
from rest_framework import mixins
from .permissions import IsTeacherUser
from . import serializers


class ProfileViewSet(viewsets.GenericViewSet,
                     mixins.UpdateModelMixin):
    serializer_class = serializers.ProfileSerializer
    queryset = Profile.objects.all()


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
    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return serializers.StatisticsReadSerializer
        elif self.action == "update":
            return serializers.StatisticsPutSerializer
        return serializers.StatisticsPostSerializer

    def get_queryset(self):
        return Statistics.objects.filter(user=self.request.user)


class TaskViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin):
    permission_classes = [IsTeacherUser, ]
    serializer_class = serializers.TaskWithoutAnswersSerializer

    def get_queryset(self):
        return Task.objects.filter(exam__author=self.request.user)


class AnswerViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin):
    permission_classes = [IsTeacherUser, ]
    serializer_class = serializers.AnswerWithTaskSerializer

    def get_queryset(self):
        return Answer.objects.filter(task__exam__author=self.request.user)


class ExamsMeViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin):
    serializer_class = serializers.ExamListSerializer

    def get_queryset(self):
        return Exam.objects.filter(author=self.request.user)
