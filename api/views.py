from rest_framework import viewsets
from .models import Exam
from rest_framework import mixins
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
    queryset = Exam.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.ExamWithTaskRetrieveSerializer
        elif self.action in ['create', 'update']:
            return serializers.ExamCreateSerializer
        else:
            return serializers.ExamSerializer
