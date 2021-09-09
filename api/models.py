from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    email = models.EmailField('Email', unique=True)
    is_teacher = models.BooleanField("Учитель")
    created_at = models.DateTimeField("Дата создания аккаунта", auto_now_add=True)
    updated_at = models.DateTimeField("Дата редактирования аккаунта", auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "is_teacher"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ('email', "created_at")

    def __str__(self):
        return self.email


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, verbose_name="Пользователь", related_name="profile",
                                on_delete=models.CASCADE)
    avatar = models.ImageField("Аватарка", upload_to="user/", null=True, blank=True)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return self.user.email


class Exam(models.Model):
    SUBJECT_CHOICES = [
        ("al", "Алгебра"),
        ("as", "Астрономия"),
        ("bi", "Биология"),
        ("ch", "Химия"),
        ("en", "Английский"),
        ("gm", "Геометрия"),
        ("hi", "История"),
        ("ph", "Физика"),
        ("ru", "Русский язык"),
        ("cs", "Информатика"),
        ("ss", "Обществознание"),
        ("gg", "География"),
        ("fl", "Иностранный язык"),
        ("li", "Литература"),
        ("ob", "ОБЖ"),
    ]
    CLASSROOM = [
        (1, "1 класс"),
        (2, "2 класс"),
        (3, "3 класс"),
        (4, "4 класс"),
        (5, "5 класс"),
        (6, "6 класс"),
        (7, "7 класс"),
        (8, "8 класс"),
        (9, "9 класс"),
        (10, "10 класс"),
        (11, "11 класс"),
    ]
    author = models.ForeignKey(CustomUser, verbose_name="Учитель", related_name="exams", on_delete=models.CASCADE)
    title = models.CharField("Тема", max_length=300)
    classroom = models.SmallIntegerField("Класс", choices=CLASSROOM)
    subject = models.CharField("Предмет", max_length=2, choices=SUBJECT_CHOICES)
    description = models.TextField("Описание")
    publish_time = models.DateTimeField("Время публикации", auto_now_add=True)
    edit_time = models.DateTimeField("Время изменения", auto_now=True)
    is_show = models.BooleanField("Видимость", default=True)

    class Meta:
        verbose_name = "Контрольная"
        verbose_name_plural = "Контрольные"
        ordering = ("publish_time",)

    def __str__(self):
        return self.title


class Task(models.Model):
    exam = models.ForeignKey(Exam, verbose_name="Упражнение", related_name="tasks", on_delete=models.CASCADE)
    question = models.TextField("Вопрос")

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"

    def __str__(self):
        return self.question


class Answer(models.Model):
    task = models.ForeignKey(Task, verbose_name="Ответ", related_name="answers", on_delete=models.CASCADE)
    text = models.TextField("Вариант ответа")
    is_correct = models.BooleanField("Верный")

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return self.text


class Comment(models.Model):
    exam = models.ForeignKey(Exam, verbose_name="Упражнение", related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, verbose_name="Комментатор", related_name="comments",
                               on_delete=models.CASCADE)
    text = models.TextField("Текст")
    publish_time = models.DateTimeField("Время публикации", auto_now_add=True)
    edit_time = models.DateTimeField("Время редактирования", auto_now=True)

    class Meta:
        verbose_name = "Комметарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text


class Statistics(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name="Пользователь", related_name="statistics",
                             on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, verbose_name="Упражнение", related_name="statistics", on_delete=models.CASCADE)
    grade = models.SmallIntegerField("Количество набранных баллов")
    total = models.SmallIntegerField("Общее количество баллов")
    start_time = models.DateTimeField("Начало выполнения", auto_now_add=True)
    end_time = models.DateTimeField("Конец выполнения", auto_now=True)

    class Meta:
        verbose_name = "Статистика"
        verbose_name_plural = "Статистика"

    def __str__(self):
        return self.exam.title


class ErrorStatistics(models.Model):
    statistics = models.ForeignKey(Statistics, verbose_name="Ошибки", related_name="errors",
                                   on_delete=models.CASCADE)
    question = models.TextField("Вопрос")

    class Meta:
        verbose_name = "Ошибка"
        verbose_name_plural = "Ошибки"

    def __str__(self):
        return self.question
