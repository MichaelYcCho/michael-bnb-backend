from typing import Any

from rest_framework import serializers


def create_serializer_class(name: str, fields: dict) -> type:
    return type(name, (serializers.Serializer,), fields)


def inline_serializer(*, fields: dict, data: Any = None, **kwargs: dict) -> type:
    serializer_class = create_serializer_class(name="", fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)
