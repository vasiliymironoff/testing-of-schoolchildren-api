from . import models
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField


class ProfileSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField()

    class Meta:
        model = models.Profile
        fields = ("avatar", )


class UserMeSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source="profile.avatar", read_only=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    is_teacher = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.CustomUser
        fields = ("first_name",
                  "last_name",
                  "email",
                  "is_teacher",
                  "avatar")


class AuthorSerializer(serializers.ModelSerializer):
    """Минимальная информация об авторе"""
    avatar = serializers.ImageField(source="profile.avatar")

    class Meta:
        model = models.CustomUser
        fields = ("id",
                  "first_name",
                  "last_name",
                  "email",
                  "avatar")


class CommentForExamSerializer(serializers.ModelSerializer):
    """
    Серилайзер для Comment с минимальной информацией
    об авторе для Exam retrive
    """
    author = AuthorSerializer()

    class Meta:
        model = models.Comment
        fields = ("id",
                  "author",
                  "text",
                  "publish_time",
                  "edit_time")


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Comment
        fields = ("id",
                  "author",
                  "text",
                  "exam",
                  "publish_time",
                  "edit_time", )


class AnswerSerializer(serializers.ModelSerializer):
    """Серилайзер для Answer"""
    class Meta:
        model = models.Answer
        fields = ("id",
                  "text",
                  "is_correct")


class TaskSerializer(serializers.ModelSerializer):
    """Сериалайзер для Task"""
    answers = AnswerSerializer(many=True)

    class Meta:
        model = models.Task
        fields = ('id',
                  'question',
                  'answers')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["many_option"] = instance.answers.filter(is_correct=True).count()
        return representation


class ExamListSerializer(serializers.ModelSerializer):
    """Сериалайзер для списка Exercise"""
    author = AuthorSerializer()

    class Meta:
        model = models.Exam
        fields = ('id',
                  "author",
                  "title",
                  "classroom",
                  "subject",
                  "publish_time",
                  "edit_time",)


class ExamRetrieveSerializer(serializers.ModelSerializer):
    """Сериалайзер для Exercise с полной информацией, но без Task"""
    author = AuthorSerializer()
    comments = CommentForExamSerializer(many=True)

    class Meta:
        model = models.Exam
        fields = ('id',
                  "author",
                  "title",
                  "classroom",
                  "description",
                  "subject",
                  "publish_time",
                  "edit_time",
                  "comments")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["count_task"] = instance.tasks.count()
        return representation


class ExamSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    tasks = TaskSerializer(many=True)

    class Meta:
        model = models.Exam
        fields = ('id',
                  "author",
                  "title",
                  "classroom",
                  "subject",
                  "description",
                  "publish_time",
                  "edit_time",
                  "tasks",)

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
        tasks_data = validated_data.pop("tasks")
        tasks = instance.tasks.all()
        tasks = list(tasks)
        instance.title = validated_data.get("title", instance.title)
        instance.classroom = validated_data.get("classroom", instance.classroom)
        instance.subject = validated_data.get("subject", instance.subject)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        for task_data in tasks_data:
            task = tasks.pop(0)
            answers_data = task_data.pop("answers")
            answers = task.answers.all()
            answers = list(answers)
            task.question = task_data.get("question", task.question)
            task.save()
            for answer_data in answers_data:
                answer = answers.pop(0)
                answer.text = answer_data.get("text", answer.text)
                answer.is_correct = answer_data.get("is_correct", answer.is_correct)
                answer.save()
        return instance

# {
#   "title": "string",
#   "classroom": 0,
#   "subject": "al",
#   "description": "Описание",
#   "tasks": [
#      {
#        "question": "Вопрос?",
#        "answers": [
#           {
#              "text": "text",
#              "is_correct": true
#           }
#         ]
#      }
#   ]
# }

# {
#     "id": 1,
#     "title": "Название",
#     "classroom": 4,
#     "subject": "en",
#     "description": "123",
#     "tasks": [
#         {
#             "id": 1,
#             "question": "Как называется",
#             "answers": [
#                 {
#                     "id": 1,
#                     "text": "1",
#                     "is_correct": true
#                 },
#                 {
#                     "id": 2,
#                     "text": "2",
#                     "is_correct": false
#                 },
#                 {
#                     "id": 3,
#                     "text": "3",
#                     "is_correct": true
#                 }
#             ]
#         },
#         {
#             "id": 2,
#             "question": "44444",
#             "answers": [
#                 {
#                     "id": 4,
#                     "text": "9999999999",
#                     "is_correct": false
#                 },
#                 {
#                     "id": 5,
#                     "text": "7",
#                     "is_correct": true
#                 },
#                 {
#                     "id": 6,
#                     "text": "8",
#                     "is_correct": false
#                 },
#                 {
#                     "id": 7,
#                     "text": "9999999999999999",
#                     "is_correct": false
#                 }
#             ]
#         }
#     ]
# }


class StatisticsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Statistics
        fields = ("id",
                  "user",
                  "exam",
                  "grade",
                  "total")

    def create(self, validated_data):
        validated_data["grade"] = 0
        stat = models.Statistics.objects.create(**validated_data)
        return stat

    def update(self, instance, validated_data):
        instance.grade = validated_data.get("grade", instance.grade)
        instance.save()
        return instance
