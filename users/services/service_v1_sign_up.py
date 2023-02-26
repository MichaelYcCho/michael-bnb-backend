from users.models import User
from utils.exceptions.exception import UserExceptions


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
            raise UserExceptions.PasswordNotMatch

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
