from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import FormView, DetailView

from .models import *
from .forms import *


def index(request):
    if request.user.is_authenticated:
        return render(request, 'app/main.html')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['login']
                password = form.cleaned_data['password']
                user = authenticate(request,
                                    username=username,
                                    password=password)
                if user is not None:
                    login(request, user)
                    next_page = request.POST.get('next_page')
                    if next_page:
                        return redirect(next_page)
                    else:
                        return redirect(index)
                else:
                    form.add_error('password', 'Неверный логин или пароль')
        else:
            form = LoginForm()
        next_page = request.GET.get('next', '')

        return render(request, 'app/index.html',
                      {'form': form, 'next_page': next_page})


def login_view(request):
    if 'username' in request.POST and 'password' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,
                            username=username,
                            password=password)
        if user is not None:
            login(request, user)
            return redirect(index)

    return redirect(index)


def logout_view(request):
    logout(request)
    return redirect(index)


@login_required
def settings_general_subjects(request):
    if request.method == 'POST':
        form = AddSubjectForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            s = Subject(**data)
            s.save()
            redirect(settings_general_subjects)
    else:
        form = AddSubjectForm()

    subs = Subject.objects.all()

    return render(request, 'app/settings_general_subjects.html',
                  {'form': form, 'subs': subs})


@login_required
def settings_general_levels(request):
    return render(request, 'app/settings_general_levels.html')


@method_decorator(login_required, 'dispatch')
class AgeCategoryAdd(FormView):
    template_name = 'app/settings_general_ages.html'
    form_class = AddAgeCategoryForm
    success_url = reverse_lazy('settings_general_ages')

    def form_valid(self, form):
        AgeCategory.objects.create(**form.cleaned_data)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ages"] = AgeCategory.objects.all()
        return context


@login_required
def settings_members_status(request):
    if request.method == 'POST':
        form = AddStatusForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            s = Status(**data)
            s.save()
            return redirect(settings_members_status)
    else:
        form = AddStatusForm()

    statuses = Status.objects.all()
    return render(request, 'app/settings_members_status.html',
                  {'form': form, 'statuses': statuses})


@login_required
def settings_members_roles(request):
    if request.method == 'POST':
        form = AddRoleForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            role = Role(**data)
            role.save()
            return redirect(settings_members_roles)
    else:
        form = AddRoleForm()

    roles = Role.objects.all()
    return render(request, 'app/settings_members_roles.html',
                  {'form': form, 'roles': roles})


@login_required
def settings_members_perms(request, role_id=None):
    if role_id:
        cur_role = Role.objects.get(id=role_id)
        if request.method == 'POST':
            form = RolePermsForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                for attr, value in data.items():
                    setattr(cur_role, attr, value)
                cur_role.save()
                return redirect(settings_members_perms, role_id)
        else:
            form = RolePermsForm(cur_role.__dict__)
    else:
        cur_role = Role.objects.order_by('id').first()
        return redirect(settings_members_perms, cur_role.id)
    roles = Role.objects.all()
    return render(request, 'app/settings_members_perms.html',
                  {'roles': roles, 'cur_role': cur_role,
                   'form': form})


@login_required
def company_members(request):
    members = Member.objects.all()
    return render(request, 'app/company_members.html',
                  {'members': members})


@login_required
def company_members_add(request):
    if request.method == 'POST':
        form = AddMemberForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            fields = {key: data[key] for key in [
                'name', 'surname', 'patronymic',
                'email', 'gender', 'role',
            ]}
            user = User.objects.create_user(data['email'],
                                            email=data['email'],
                                            password=data['password'])
            member = Member(**fields)
            member.user = user
            member.save()
            return redirect(company_members)
    else:
        form = AddMemberForm()
    return render(request, 'app/company_members_add.html',
                  {'form': form})


@login_required
def member_profile(request, uid):
    member = Member.objects.get(id=uid)
    return render(request, 'app/company_member_profile.html',
                  {'member': member})


@login_required
def company_schools(request):
    schools = School.objects.all()
    return render(request, 'app/company_schools.html',
                  {'schools': schools})


@method_decorator(login_required, 'dispatch')
class CompanySchoolsAdd(FormView):
    template_name = 'app/company_schools_add.html'
    form_class = AddSchoolForm
    success_url = '/company/schools'

    def form_valid(self, form):
        School.objects.create(**form.cleaned_data)
        return super().form_valid(form)


@method_decorator(login_required, 'dispatch')
class CompanySchoolsAddRoom(FormView):
    template_name = 'app/company_schools_add_room.html'
    form_class = AddRoomForm
    success_url = '/company/schools'

    def get_initial(self):
        initial = super().get_initial()
        if 'sid' in self.kwargs:
            sid = self.kwargs['sid']
            school = School.objects.get(id=sid)
            initial['school'] = school
        return initial

    def form_valid(self, form):
        Room.objects.create(**form.cleaned_data)
        return super().form_valid(form)


@login_required
def company_camps(request):
    camps = Camps.objects.all()
    return render(request, 'app/company_camps.html',
                  {'camps': camps})


@login_required
def company_salaries(request):
    peoples = People.objects.all()
    return render(request, 'app/company_salaries.html',
                  {'peoples': peoples})

class CompanySalaryAdd(FormView):
    template_name = 'app/company_salaries_add.html'
    form_class = AddSalaryForm
    success_url = '/company/salaries'

    def form_valid(self, form):
        People.objects.create(**form.cleaned_data)
        return super().form_valid(form)



@method_decorator(login_required, 'dispatch')
class CompanyCampsAdd(FormView):
    template_name = 'app/company_camps_add.html'
    form_class = AddCampForm
    success_url = '/company/camps'

    def form_valid(self, form):
        Camps.objects.create(**form.cleaned_data)
        return super().form_valid(form)


@login_required
def learning_students(request):
    students = Student.objects.all()
    return render(request, 'app/learning_students.html',
                  {'students': students})


@login_required
def learning_students_add(request):
    if request.method == 'POST':
        form = AddStudentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            student = Student(**data)
            student.save()
            return redirect(learning_students)
    else:
        form = AddStudentForm()
    return render(request, 'app/learning_students_add.html',
                  {'form': form})


def learning_groups(request):
    groups = Group.objects.all()
    return render(request, 'app/learning_groups.html',
                  {'groups': groups})


@method_decorator(login_required, 'dispatch')
class LearningGroupsAdd(FormView):
    template_name = 'app/learning_groups_add.html'
    form_class = AddGroupForm
    success_url = reverse_lazy('learning_groups')

    def form_valid(self, form):
        group = Group(**form.cleaned_data)
        group.status = Group.FORMING
        group.save()
        return super().form_valid(form)


@method_decorator(login_required, 'dispatch')
class LearningGroupsDetails(DetailView):
    model = Group
    context_object_name = 'group'
    template_name = 'app/learning_groups_details.html'


@method_decorator(login_required, 'dispatch')
class LearningGroupStudentAdd(FormView):
    template_name = 'app/learning_groups_add_student.html'
    form_class = AddGroupStudentForm

    def form_valid(self, form):
        data = form.cleaned_data
        group = data['group']
        students = data['students']
        group.students.add(*students)
        group.save()
        self.success_url = reverse('learning_groups_details', kwargs={'pk': group.pk})
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            group = Group.objects.get(pk=pk)
            initial['group'] = group
        return initial


@method_decorator(login_required, 'dispatch')
class LearningGroupScheduleAdd(FormView):
    template_name = 'app/learning_groups_add_schedule.html'
    form_class = AddGroupScheduleForm

    def form_valid(self, form):
        data = form.cleaned_data
        group = data['group']
        fields = {k: data[k] for k in ['group', 'time', 'start_date', 'count']}
        fields['weekday'] = fields['start_date'].weekday()
        schedule = Schedule(**fields)
        schedule.save()
        schedule.teachers.set(data['teachers'])

        self.success_url = reverse('learning_groups_details', kwargs={'pk': group.pk})
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            group = Group.objects.get(pk=pk)
            initial['group'] = group
        return initial