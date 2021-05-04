from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, email, user_name, password=None):
        """
        creates a user with given email and password
        """
        if not email:
            raise ValueError('user must have a email address')

        user = self.model(
            email=self.normalize_email(email),
            user_name= user_name
        )
        user.set_password(password)
        user.save(self._db)
        return user

    def create_staffuser(self, email, user_name, password):
        """
        creates a user with staff permissions
        """
        user = self.create_user(
            email=email,
            user_name = user_name,
            password=password
        )
        user.active = True
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email,user_name, password):
        """
        creates a superuser with email and password
        """
        user = self.create_user(
            email=email,
            user_name = user_name,
            password=password
        )
        user.active = True
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email address',
        max_length=255,
        unique=True
    )

    user_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=True)  # <- admin user, not super user
    admin = models.BooleanField(default=False)  # <- super user

    # notice the absence of password field
    # that is built in

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']  # <- email and password are required by default

    def get_full_name(self):
        return str(self.email)

    def has_perm(self, perm, obj=None):
        """Does the user has a specific permission"""
        return True

    def has_module_perms(self, app_lable):
        """Does the user has permission to view a specific app"""
        return True

    @property
    def is_staff(self):
        """Is the user a staff member"""
        return self.staff

    @property
    def is_admin(self):
        """Is the user a admin member"""
        return self.admin

    @property
    def is_active(self):
        """Is the user active"""
        return self.active

    # hook the user manager to objects
    objects = UserManager()
