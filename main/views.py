# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView ,FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import  redirect
from django.contrib.auth import  login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .models import App
from .forms import AppForm
from django.http import HttpResponse
from .tasks import run_appium_test


class LoginPage(LoginView):
    template_name = "registration/login.html"
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('dashboard')


class RegisterPage(FormView):
    template_name='registration/register.html'  
    form_class=UserCreationForm  
    redirect_authenticated_user = True
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        user=form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)
    def form_invalid(self, form):
        return super(RegisterPage, self).form_invalid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('dashboard')
        return super(RegisterPage, self).get(*args, **kwargs)

class AllAppsView(LoginRequiredMixin, ListView):
    model = App
    template_name = 'apps/all-apps.html'
    context_object_name = 'apps'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apps'] = context['apps'].filter(uploaded_by=self.request.user)
        return context

class AppCreateView(LoginRequiredMixin,CreateView):
    model = App
    form_class = AppForm
    template_name = 'apps/app_form.html'
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)

class AppUpdateView(LoginRequiredMixin, UpdateView):
    model = App
    form_class = AppForm
    template_name = 'apps/app_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)

class AppDeleteView(LoginRequiredMixin, DeleteView):
    model = App
    template_name = 'apps/app_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

    def test_func(self):
        app = self.get_object()
        return self.request.user == app.uploaded_by
class AppDetailView(LoginRequiredMixin,DetailView):
    model = App
    template_name = 'apps/view-app.html'



def start_appium_test_view(request,pk):
    # print("========== " ,pk)
    app=App.objects.get(pk=pk)
    # print("==== ,",app.name,app.apk_file_path)
    run_appium_test.delay(pk)
    return HttpResponse("Appium test started.")
