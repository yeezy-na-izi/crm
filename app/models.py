import datetime

from django.contrib.auth.models import User
from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10)
    level_count = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=50)


class Role(models.Model):
    name = models.CharField(max_length=50)
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class AgeCategory(models.Model):
    name = models.CharField(max_length=50)

    start = models.PositiveSmallIntegerField(null=True)
    end = models.PositiveSmallIntegerField(null=True)


class Person(models.Model):
    class Meta:
        abstract = True

    MALE = 'M'
    FEMALE = 'F'

    GENDERS = (
        ('', 'Не указан'),
        (MALE, 'Мужской'),
        (FEMALE, 'Женский'),
    )

    surname = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50, blank=True)

    gender = models.CharField(max_length=1, blank=True, choices=GENDERS)
    birthday = models.DateField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    email = models.EmailField()
    cell_phone = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    social = models.CharField(max_length=250, blank=True)
    skype = models.CharField(max_length=50, blank=True)

    def get_full_name(self):
        return self.surname + ' ' + self.name + ' ' + self.patronymic

    def __str__(self):
        return self.get_full_name()


class Member(Person):
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL,
                               null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Student(Person):
    cont_role = models.CharField(max_length=50, blank=True)
    cont_surname = models.CharField(max_length=50, blank=True)
    cont_name = models.CharField(max_length=50, blank=True)
    cont_patronymic = models.CharField(max_length=50, blank=True)
    cont_email = models.EmailField(blank=True)
    cont_cell_phone = models.CharField(max_length=20, blank=True)


class School(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=250, blank=True)


class Camps(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=250, blank=True)
    children_count = models.PositiveSmallIntegerField()

class People (models.Model):
    name = models.CharField(max_length=50)
    duty = models.CharField(max_length=250, blank=True)
    salary = models.PositiveSmallIntegerField(null=True)


class Room(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250, blank=True)
    capacity = models.PositiveSmallIntegerField(null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)


class Group(models.Model):
    FORMING = 'f'
    WORKING = 'w'
    FINISHED = 'e'
    SUSPENDED = 's'

    GROUP_STATUS = (
        (FORMING, 'Формируется'),
        (WORKING, 'Работает'),
        (SUSPENDED, 'Приостановлена'),
        (FINISHED, 'Завершена'),
    )

    status = models.CharField(max_length=1, choices=GROUP_STATUS)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    level = models.PositiveSmallIntegerField()
    capacity = models.PositiveSmallIntegerField(null=True)
    name = models.CharField(max_length=50, blank=True)
    students = models.ManyToManyField(Student, related_name='groups')

    def __str__(self):
        return self.name


class Schedule(models.Model):
    WEEKDAYS = (
        (0, 'Пн'),
        (1, 'Вт'),
        (2, 'Ср'),
        (3, 'Чт'),
        (4, 'Пт'),
        (5, 'Сб'),
        (6, 'Вс'),
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='schedules')
    weekday = models.PositiveSmallIntegerField(choices=WEEKDAYS)
    time = models.TimeField()
    start_date = models.DateField()
    count = models.PositiveSmallIntegerField()
    teachers = models.ManyToManyField(Member, related_name='schedules')

    def get_end_date(self):
        return self.start_date + datetime.timedelta(weeks=self.count)
