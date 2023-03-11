from typing import Type

from pydantic import BaseModel
from rest_framework import serializers


class PydanticModelSerializer(serializers.Serializer):
    """
    Serializer that uses Pydantic models instead of DRF serializers
    """

    # POST, PUT과 같이 데이터 변경이 있을 때 client에서 들어오는 데이터를 저장 전에 핸들링할 수 있는 메서드
    def to_internal_value(self, data):
        pydantic_model = self.get_py_model()
        # convert request data to Pydantic model
        pydantic_data = pydantic_model.parse_obj(data)
        # return Pydantic model as a dict
        return pydantic_data.dict()

    # GET, POST, PUT과 같이 데이터 변경이 있고 난 후에 client에 값을 변환해서 보여줄 경우 사용하는 메서드
    def to_representation(self, instance):
        pydantic_model = self.get_py_model()
        # convert Django model to Pydantic model
        pydantic_instance = pydantic_model.from_orm(instance)
        # return Pydantic model as a dict
        return pydantic_instance.dict()

    def get_py_model(self) -> Type[BaseModel]:
        raise NotImplementedError("Must implement get_py_model in subclass")
