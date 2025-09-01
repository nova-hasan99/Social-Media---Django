from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Try logging in with email
        if '@' in username:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
        else:
            # Try logging in with username
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None

        # Check password and return user if valid
        if user and user.check_password(password):
            return user
        return None
