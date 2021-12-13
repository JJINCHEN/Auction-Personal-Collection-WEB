from django.contrib.auth.backends import ModelBackend

from .models import UserProfile


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.filter(username=username)
            if len(user) == 0:
                user = UserProfile.objects.filter(email=username)
            if len(user) == 0:
                return None
            else:
                user = user[0]
            if user.check_password(password):
                return user

        except Exception as e:
            return None
