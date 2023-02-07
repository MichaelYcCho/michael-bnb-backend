from django.db import models
from model_utils import Choices


class GenderChoices(models.IntegerChoices):
    """성별 CHOICES"""

    MAIL = 0, "남성"
    FEMAIL = 1, "여성"


class LanguageChoices(models.TextChoices):
    """언어"""

    KR = ("KR", "Korean")
    EN = ("EN", "English")


class CurrencyChoices(models.TextChoices):
    """통화단위"""

    WON = "won", "Korean Won"
    USD = "usd", "Dollar"


class SNS_TYPE(models.TextChoices):
    """소셜 플랫폼"""

    KAKAO = ("K", "KAKAO")
    NAVER = ("N", "NAVER")
    GOOGLE = ("G", "GOOGLE")
    GIT_HUB = ("GH", "GIT_HUB")
