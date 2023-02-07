from datetime import datetime

from pytz import timezone


def get_kst_now() -> datetime:
    """한국시간 반환"""

    KST = timezone("Asia/Seoul")

    now = datetime.now()
    return now.astimezone(KST)
