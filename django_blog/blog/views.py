from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm, User


# Create your views here.
class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'blog/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
        return render(request, 'blog/register.html', {'form': form})


class ProfileUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = ProfileUpdateForm(instance=request.user)
        return render(request, 'blog/profile.html', {'form': form})

    def post(self, request):
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, 'blog/profile.html', {'form': form})
