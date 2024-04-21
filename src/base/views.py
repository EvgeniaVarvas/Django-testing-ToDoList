from django.shortcuts import render, redirect

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task

# Create your views here.

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task_list')
        return super(RegisterPage, self).get(*args, **kwargs)

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('task_list')

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'base/task_list.html'
    ordering = ['-created']

    def get_queryset(self):
        # Получаем QuerySet всех задач
        queryset = super().get_queryset()
        
        # Проверяем, аутентифицирован ли пользователь
        if self.request.user.is_authenticated:
            # Если пользователь аутентифицирован, фильтруем задачи по пользователю
            queryset = queryset.filter(user=self.request.user)
        
        return queryset

    def get_context_data(self, **kwargs):
        # Получаем контекст данных
        context = super().get_context_data(**kwargs)
        
        # Добавляем дополнительные данные
        context['count'] = self.get_queryset().filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)

        context['search_input'] = search_input
        return context


class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task_detail.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
            
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    template_name = 'base/task_form.html'
    success_url = reverse_lazy('task_list')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task_delete.html'
    success_url = reverse_lazy('task_list')
