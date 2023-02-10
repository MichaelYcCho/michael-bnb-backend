from rest_framework.status import HTTP_400_BAD_REQUEST

from users.models import User


class SignUpService:
    def __init__(self, validated_data: dict) -> None:
        self.name = validated_data["name"]
        self.username = validated_data["username"]
        self.password = validated_data["password"]
        self.password_confirm = validated_data["password_confirm"]
        self.email = validated_data["email"]
        self.phone = validated_data["phone"]

    def validate_password(self) -> None:

        if self.password != self.password_confirm:
            raise HTTP_400_BAD_REQUEST("비밀번호가 일치하지 않습니다.")

    def create_user(self) -> User:
        user = User.objects.create(
            username=self.username,
            name=self.name,
            email=self.email,
            phone=self.phone,
        )
        user.set_password(self.password)
        user.save()
        return user
