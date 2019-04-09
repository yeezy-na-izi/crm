from django import forms
from django.core import validators

from .models import Member, Role, Student, School, Subject, Group, Schedule

error_messages = {
    'required': 'Необходимо заполнить',
    'invalid': 'Неверный формат'
}


class LoginForm(forms.Form):
    login = forms.CharField(
        error_messages=error_messages
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages=error_messages
    )


class AddSubjectForm(forms.Form):
    name = forms.CharField(
        label='Название',
        max_length=50,
        error_messages=error_messages
    )
    symbol = forms.SlugField(
        label='Обозначение',
        max_length=10,
        error_messages=error_messages
    )
    level_count = forms.IntegerField(
        label='Кол-во уровней',
        validators=[validators.MinValueValidator(1)],
        error_messages={**error_messages,
                        'min_value': 'Требуется положительное целое число'}
    )


class AddStatusForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        error_messages=error_messages
    )


class AddRoleForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        error_messages=error_messages
    )


class AddAgeCategoryForm(forms.Form):
    name = forms.CharField(
        label='Название',
        max_length=50,
        error_messages=error_messages
    )
    start = forms.IntegerField(
        label='Начальный возраст',
        validators=[validators.MinValueValidator(0)],
        required= False,
        error_messages={**error_messages,
                        'min_value': 'Требуется положительное целое число'}
    )
    end = forms.IntegerField(
        label='Конечный возраст',
        validators=[validators.MinValueValidator(1)],
        required=False,
        error_messages={**error_messages,
                        'min_value': 'Требуется положительное целое число'}
    )


class RolePermsForm(forms.Form):
    is_teacher = forms.BooleanField(label='Является учителем',
                                    required=False)


class AddMemberForm(forms.Form):
    surname = forms.CharField(max_length=50, label='Фамилия',
                              error_messages=error_messages)
    name = forms.CharField(max_length=50, label='Имя',
                           error_messages=error_messages)
    patronymic = forms.CharField(max_length=50, label='Отчество',
                                 required=False,
                                 error_messages=error_messages)

    email = forms.EmailField()

    gender = forms.ChoiceField(choices=Member.GENDERS, label='Пол',
                               required=False,
                               error_messages=error_messages)

    role = forms.ModelChoiceField(queryset=Role.objects.all(), label='Роль',
                                  empty_label='...')

    password = forms.CharField(max_length=50, label='Пароль')


class AddStudentForm(forms.Form):
    surname = forms.CharField(max_length=50, label='Фамилия',
                              error_messages=error_messages)
    name = forms.CharField(max_length=50, label='Имя',
                           error_messages=error_messages)
    patronymic = forms.CharField(max_length=50, label='Отчество',
                                 required=False,
                                 error_messages=error_messages)

    gender = forms.ChoiceField(choices=Student.GENDERS, label='Пол',
                               required=False,
                               error_messages=error_messages)

    email = forms.EmailField(required=False)

    cont_role = forms.CharField(max_length=50, label='Кем приходится',
                                required=False,
                                error_messages=error_messages)
    cont_surname = forms.CharField(max_length=50, label='Фамилия',
                                   required=False,
                                   error_messages=error_messages)
    cont_name = forms.CharField(max_length=50, label='Имя',
                                required=False,
                                error_messages=error_messages)
    cont_patronymic = forms.CharField(max_length=50, label='Отчество',
                                      required=False,
                                      error_messages=error_messages)
    cont_email = forms.EmailField(required=False, label='Email')
    cont_cell_phone = forms.CharField(max_length=20, label='Телефон',
                                      required=False)


class AddSchoolForm(forms.Form):
    name = forms.CharField(max_length=50, label='Название',
                           error_messages=error_messages)

    address = forms.CharField(max_length=50, label='Адрес',
                              required=False,
                              error_messages=error_messages)


class AddCampForm(forms.Form):
    name = forms.CharField(max_length=50, label='Название',
                           error_messages=error_messages)

    address = forms.CharField(max_length=50, label='Адрес',
                              required=False,
                              error_messages=error_messages)

    children_count = forms.IntegerField(
        label='Количество участников',
        validators=[validators.MinValueValidator(1)],
        error_messages={**error_messages,
                        'min_value': 'Требуется положительное целое число'})

class AddSalaryForm(forms.Form):
    name = forms.CharField(max_length=50, label='Имя',
                           error_messages=error_messages)

    duty = forms.CharField(max_length=50, label='Должность',
                              required=False,
                              error_messages=error_messages)

    salary = forms.IntegerField(
        label='Рубли',
        validators=[validators.MinValueValidator(1)],
        error_messages={**error_messages,
                        'min_value': 'Требуется положительное целое число'})


class AddRoomForm(forms.Form):
    name = forms.CharField(max_length=50, label='Название',
                           error_messages=error_messages)

    description = forms.CharField(max_length=50, label='Описание',
                                  required=False,
                                  error_messages=error_messages)

    capacity = forms.IntegerField(
        validators=[validators.MinValueValidator(1)],
        error_messages={**error_messages,
                        'min_value': 'Требуется положительное целое число'})

    school = forms.ModelChoiceField(queryset=School.objects.all(), label='Филиал',
                                    empty_label='...')


class AddGroupForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), label='Предмет',
                                     empty_label='...')

    level = forms.IntegerField(
        label='Уровень',
        validators=[validators.MinValueValidator(1)],
        error_messages={**error_messages,
                        'min_value': 'Требуется положительное целое число'}
    )

    capacity = forms.IntegerField(
        label="Вместимость",
        required=False,
        validators=[validators.MinValueValidator(1)],
        error_messages={**error_messages,
                        'min_value': 'Требуется положительное целое число'})

    name = forms.CharField(max_length=50, label='Название',
                           required=False,
                           error_messages=error_messages)


class AddGroupStudentForm(forms.Form):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), label='Группа',
                                   empty_label='...')
    students = forms.ModelMultipleChoiceField(queryset=Student.objects.all(), label='Ученики')


class AddGroupScheduleForm(forms.Form):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), label='Группа',
                                   empty_label='...')

    # weekday = forms.ChoiceField(label='День недели', choices=Schedule.WEEKDAYS)

    time = forms.TimeField(label='Время начала')
    start_date = forms.DateField(label='Дата первого занятия',
                                 input_formats=['%d.%m.%Y'])

    count = forms.IntegerField(label='Кол-во занятий',
                                 validators=[validators.MinValueValidator(1)])

    teachers = forms.ModelMultipleChoiceField(queryset=Member.objects.all(), label='Пеподаватели')
