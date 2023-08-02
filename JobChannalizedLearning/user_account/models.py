from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, user_role, plan, email=None, password=None):
        if not username:
            raise ValueError('Valid username should be provided')
        base_user = self.model(
            email=self.normalize_email(email),
            username=username,
            user_role=user_role,
            plan=plan
        )
        base_user.set_password(password)
        base_user.save(using=self._db)
        return base_user

    def create_superuser(self, email, username, password, user_role, plan):
        super_user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            user_role=user_role,
            plan=plan
        )
        super_user.is_admin = True
        super_user.is_staff = True
        super_user.is_superuser = True
        super_user.save(using=self._db)
        return super_user


class User(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    user_choices = [
        ('STUDENT', 'Student'),
        ('MENTOR', 'Mentor'),
        ('ADMIN', 'Admin')
    ]
    plan_choices = [
        ('Basic', 'Basic'),
        ('Super', 'Super'),
        ('Pro', 'Pro')
    ]
    email = models.EmailField(max_length=60, unique=True)
    user_role = models.CharField(max_length=10, choices=user_choices)
    plan = models.CharField(max_length=10, choices=plan_choices, default='Basic')
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'user_role']
    objects = UserManager()

    def __str__(self):
        return self.username

    # To check for permissions while logging in
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # We are saying that the current user has permissions to view this application.
    def has_module_perms(self, app_label):
        return True
