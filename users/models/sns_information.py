from django.db import models
from model_utils.models import TimeStampedModel

from users.models.users import User
from utils.choices import SNS_TYPE


class SNSInformation(TimeStampedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="사용자",
        related_name="user_sns_info",
    )
    sns_type = models.CharField(
        choices=SNS_TYPE.choices, max_length=5, verbose_name="플랫폼"
    )
    sns_id = models.CharField(max_length=100, verbose_name="소셜 계정", blank=True)
    email = models.CharField(max_length=255, verbose_name="이메일", blank=True)
    is_active = models.BooleanField(verbose_name="사용 여부", default=True)
