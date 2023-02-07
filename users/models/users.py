from django.db import models
from django.contrib.auth.models import AbstractUser
from model_utils.models import TimeStampedModel

from utils.choices import GenderChoices, LanguageChoices, CurrencyChoices


class User(TimeStampedModel):
    email = models.CharField(verbose_name="이메일", max_length=255)
    first_name = models.CharField(
        max_length=150,
    )
    last_name = models.CharField(
        max_length=150,
    )
    avatar = models.URLField(blank=True)
    mobile_corp = models.CharField(
        max_length=4, blank=True, null=True, verbose_name="통신사"
    )
    phone = models.CharField(verbose_name="전화 번호", max_length=50, blank=True)
    birth = models.CharField(verbose_name="생년 월일", max_length=10, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
        blank=True,
    )

    language = models.CharField(
        max_length=2,
        choices=LanguageChoices.choices,
    )
    currency = models.CharField(
        max_length=5,
        choices=CurrencyChoices.choices,
    )
    is_host = models.BooleanField(default=False)


class AdminUser(AbstractUser):

    first_name = models.CharField(
        max_length=150,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    name = models.CharField(
        max_length=150,
        default="",
    )
