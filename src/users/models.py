from app.utils import upload_image_path
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False,
                            blank=False)
    description = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to=upload_image_path, null=True,
                             blank=False)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Non-Binary', 'Non-Binary'),
        ('Transgender', 'Transgender'),
        ('Other', 'Other'),
    )

    ACTIVITY_CHOICES = (
        ('Law Explorers', 'Law Explorers'),
    )

    REQUIRED_FIELDS = []  # Only when create superuser(admin)
    USERNAME_FIELD = 'email'

    username = None
    email = models.EmailField(unique=True)
    age = models.IntegerField(null=True, blank=True, default=99,
                              validators=[MaxValueValidator(99),
                                          MinValueValidator(13)])
    gender = models.CharField(max_length=32, null=True, blank=True,
                              choices=GENDER_CHOICES)
    guardian_email = models.EmailField(null=True, blank=True)
    activity = models.CharField(max_length=32, null=True, blank=True,
                                choices=ACTIVITY_CHOICES)
    team = models.ForeignKey(Team, on_delete=models.PROTECT,
                             null=True, blank=False)
    total_points = models.IntegerField(default=0, null=False, blank=False)
    first_login = models.BooleanField(default=True)
    accepted_terms_cond = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)

    objects = UserManager()

    __original_accepted_terms_cond = None

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.__original_accepted_terms_cond = self.accepted_terms_cond

    def __str__(self):
        return self.email

    # def save(self, *args, **kwargs):
    #     if self.__original_accepted_terms_cond and len(kwargs) == 0:
    #         self.accepted_terms_cond = False
    #     super().save(args, kwargs)


class UserProxy(User):

    class Meta:
        proxy = True
        verbose_name = 'Admin'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_superuser = True
        self.is_staff = True

