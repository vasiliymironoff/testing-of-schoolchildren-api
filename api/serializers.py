from . import models
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    """Минимальная информация об авторе"""
    avatar = serializers.ImageField(source="profile.avatar")

    class Meta:
        model = models.CustomUser
        fields = ("id", "first_name", "last_name", "email", "avatar")


class ExamSerializer(serializers.ModelSerializer):
    """Только exercise"""

    class Meta:
        model = models.Exam
        fields = "__all__"


class ExamListSerializer(serializers.ModelSerializer):
    """Сериалайзер для списка Exercise"""

    author = AuthorSerializer()

    class Meta:
        model = models.Exam
        fields = ('id', "author", "title", "classroom", "subject", "publish_time",
                  "edit_time",)


class ExamRetrieveSerializer(serializers.ModelSerializer):
    """Сериалайзер для Exercise с полной информацией, но без Task"""
    author = AuthorSerializer()

    class Meta:
        model = models.Exam
        fields = ('id', "author", "title", "classroom", "description", "subject", "publish_time",
                  "edit_time",)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["count_task"] = instance.tasks.count()
        return representation


class AnswerReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ("id", "text", "is_correct")


class TaskReadSerializer(serializers.ModelSerializer):
    answers = AnswerReadSerializer(many=True)

    class Meta:
        model = models.Task
        fields = ('id', 'question', 'answers')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["many_option"] = instance.answers.filter(is_correct=True).count()
        return representation


class ExamWithTaskRetrieveSerializer(serializers.ModelSerializer):
    tasks = TaskReadSerializer(many=True)
    author = AuthorSerializer()

    class Meta:
        model = models.Exam
        fields = ('id', "author", "title", "classroom", "subject", "publish_time", "edit_time",
                  "tasks",)


"""
        Для тестирования
{
  "title": "string",
  "classroom": 0,
  "subject": "al",
  "description": "Описание",
  "tasks": [
     {
       "question": "Вопрос?",
       "answers": [
          {
             "text": "text",
             "is_correct": true
          }
        ]
     }
  ]
}
"""


class AnswerWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ("id", "text", "is_correct")


class TaskWriteSerializer(serializers.ModelSerializer):
    answers = AnswerWriteSerializer(many=True)

    class Meta:
        model = models.Task
        fields = ("id", 'question', "answers")


class ExamCreateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    tasks = TaskWriteSerializer(many=True)

    class Meta:
        model = models.Exam
        fields = ('id', "author", "title", "classroom", "subject",
                  "description", "publish_time", "edit_time", "tasks",)

    def create(self, validated_data):
        tasks = validated_data.pop("tasks")
        exam = models.Exam.objects.create(**validated_data)
        for task in tasks:
            answers = task.pop("answers")
            elem = models.Task.objects.create(exam=exam, **task)
            for answer in answers:
                models.Answer.objects.create(task=elem, **answer)
        return exam

    def update(self, instance, validated_data):
        pass
