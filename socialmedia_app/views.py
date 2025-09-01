from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import random
from django.http import Http404
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth import login, get_backends
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.views import View

from .forms import PostForm, RegistrationForm, ProfileUpdateForm
from .models import Post, Profile


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.contrib import messages
from .models import Post
from .forms import PostForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required





class home(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = list(Post.objects.all())
        random.shuffle(queryset)
        return queryset

from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from .models import Profile, Post

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profile.html'
    context_object_name = 'profile'  # Pass profile data to the template

    def get_object(self):
        """Allow anyone to view the profile"""
        return get_object_or_404(Profile, user__username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        """Pass additional data to the template"""
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object().user  # Get the profile owner

        context['profile_user'] = profile_user  # Profile owner's data
        context['posts'] = Post.objects.filter(user=profile_user).order_by('-created_at')  # Get user's posts
        context['can_edit'] = self.request.user.is_authenticated and self.request.user == profile_user  # Check if logged-in user owns the profile
        context['is_authenticated'] = self.request.user.is_authenticated  # Pass authentication status
        return context



class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'profile.html'

    def get_object(self):
        return self.request.user.profile  # Only allow users to edit their own profile

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})  # Redirect to profile page after update



class ProfilePostCreateView(LoginRequiredMixin, View):
    def post(self, request, username):
        """Create a post only if the logged-in user matches the profile"""
        profile_user = get_object_or_404(User, username=username)

        if request.user != profile_user:
            return JsonResponse({'success': False, 'message': "Unauthorized"}, status=403)

        form = PostForm(request.POST, request.FILES)  # No `or None` here
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return JsonResponse({'success': True})

        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

class ProfilePostUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Edit a post only if the logged-in user owns it"""

    def test_func(self):
        """Ensure the logged-in user is the owner of the post"""
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return self.request.user == post.user  # Allow only the owner

    def post(self, request, username, pk):
        """Handle post update"""
        profile_user = get_object_or_404(User, username=username)
        post = get_object_or_404(Post, pk=pk, user=profile_user)

        if request.user != profile_user:
            return JsonResponse({'success': False, 'message': "Unauthorized"}, status=403)

        form = PostForm(request.POST or None, request.FILES or None, instance=post)

        if form.is_valid():
            if 'image' not in request.FILES:  # Keep old image if no new one is uploaded
                form.instance.image = post.image
            form.save()
            return JsonResponse({'success': True})

        print("Form errors:", form.errors)

        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

class DeletePost(LoginRequiredMixin, View):
    """Delete a post only if the logged-in user owns it"""

    def post(self, request, username, pk):
        """Handle post deletion"""

        # Ensure the post belongs to the right user
        profile_user = get_object_or_404(User, username=username)
        post = get_object_or_404(Post, pk=pk, user=profile_user)

        if request.user != profile_user:
            messages.error(request, "Unauthorized to delete this post.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # Delete the post
        post.delete()
        messages.success(self.request, 'Post deleted successfully')
        return redirect(request.META.get('HTTP_REFERER', '/'))
        

class RegisterView(FormView):
    template_name = "register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy('home')  # Redirect after successful registration

    def form_valid(self, form):
        user = form.save()

        # Explicitly set the authentication backend
        backend = get_backends()[0]  # Use the first authentication backend
        user.backend = backend.__module__ + "." + backend.__class__.__name__

        login(self.request, user)  # Log in the new user
        messages.success(self.request, "Registration successful!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Registration failed! Please try again later.")
        return self.render_to_response(self.get_context_data(form=form))

    

class CustomLoginView(LoginView):
    def form_invalid(self, form):
        messages.error(self.request, "Invalid username/email or password. Please try again!")
        return super().form_invalid(form)
    
    def form_valid(self, form):
        messages.success(self.request, "Login successful! Welcome back.")
        return super().form_valid(form)