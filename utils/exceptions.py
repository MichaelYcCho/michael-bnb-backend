from __future__ import annotations

from typing import Any, Optional

from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404

from rest_framework import exceptions, serializers, status
from rest_framework.exceptions import ErrorDetail, APIException
from rest_framework.response import Response
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler


VALIDATION_ERROR_CODE = 999999


def custom_exception_handler(exc: Any, context: Any) -> Optional[Response]:
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    response = exception_handler(exc, context)
    if response is not None:
        try:
            exc.default_detail
        except Exception as e:
            print("커스텀 에러 핸들러 에러", e)

        error_detail = exc.args if isinstance(exc, Http404) else exc.default_detail
        data = {
            "error_code": getattr(exc, "error_code", "N/A"),
            "error_class": exc.__class__.__name__,
            "error_detail": error_detail,
        }

        if isinstance(exc, serializers.ValidationError):
            # serializer raise exception, django clean exception
            data["error_code"] = VALIDATION_ERROR_CODE

            if isinstance(response.data, list):
                if isinstance(response.data[-1], dict):
                    targets: Any = [
                        [{"string": key, "code": val[0].code} for key, val in d.items()]
                        for d in response.data
                    ]
                else:
                    targets = [
                        {"string": str(error_detail), "code": error_detail.code}
                        for error_detail in response.data
                    ]
            elif isinstance(response.data, dict):

                def get_detail(obj: object) -> object | str:
                    if isinstance(obj, ErrorDetail):
                        return obj
                    if isinstance(obj, list):
                        for o in obj:
                            if not isinstance(o, dict):
                                return get_detail(o)
                    return "N/A"

                targets = [
                    {"string": key, "code": get_detail(val)}
                    for key, val in response.data.items()
                ]
            data["targets"] = targets
            response.data = data
            print(f"serializers ValidationError {exc} {context}")
        elif isinstance(exc, Http404):
            data["error_code"] = "not_found"
            response.data.update(data)
        else:
            # custom exception
            error_detail = response.data.pop("detail", None)
            targets = [
                {"string": str(error_detail), "code": error_detail.code}
                if error_detail is not None
                else "N/A"
            ]
            data["targets"] = targets
            response.data.update(data)
    return response


class TokenExceptions:
    class TokenExpired(APIException):
        error_code = 100000
        status_code = status.HTTP_401_UNAUTHORIZED
        default_detail = "토큰이 만료되었습니다."

    class InvalidToken(APIException):
        error_code = 100001
        status_code = status.HTTP_401_UNAUTHORIZED
        default_detail = "유효하지 않은 토큰입니다."
