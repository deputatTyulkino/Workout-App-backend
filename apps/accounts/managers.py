from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from rest_framework.exceptions import ValidationError


class UserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            email = self.normalize_email(email)
            validate_email(email)
        except ValidationError:
            raise ValidationError('You must provide a valid email address')

    def password_validator(self, password):
        try:
            validate_password(password)
        except ValidationError:
            raise ValidationError('You must provide a valid password')

    def user_validator(self, email, password):
        if email:
            self.email_validator(email)
        else:
            raise ValueError('An email address is required')

        if password:
            self.password_validator(password)
        else:
            raise ValueError('A password is required')

    def superuser_validator(self, **extra_kwargs):
        extra_kwargs.setdefault('is_staff', True)
        if not extra_kwargs.get('is_staff'):
            raise ValueError('Superusers must have is_staff=True')
        return extra_kwargs

    def create_user(self, email, password, **extra_kwargs):
        self.user_validator(email, password)
        user = self.model(
            email=email, **extra_kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_kwargs):
        extra_kwargs = self.superuser_validator(**extra_kwargs)
        return self.create_user(
            email=email, password=password, **extra_kwargs
        )
