from django.db import models
import os
from django.contrib.auth.models import User


# Function to store post images in "username/post_images/"
def post_image(instance, filename):
    return os.path.join('socialmedia_app/media/', instance.user.username, 'post_images', filename)

# Function to store profile images in "username/profile_image/"
def profile_image(instance, filename):
    return os.path.join('socialmedia_app/media/', instance.user.username, 'profile_image', filename)


# Profile Model (One-to-One with User)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to=profile_image, blank=True, null=True)

    def __str__(self):
        return self.user.username

# Post Model (One user can have multiple posts)
class Post(models.Model):
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=post_image, default=None, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description[:10] + "..." if len(self.description) > 10 else self.description

