import ast
from datetime import timedelta, datetime, date

from typing import Union

from jose import jws
from config import settings
from utils.exceptions import TokenExceptions
from utils.time_utils import get_kst_now


class AuthService:
    secret = settings.JWT_SECRET_KEY
    algorithm = settings.JWT_ALGORITHM
    access_expires = timedelta(days=300)  # (hours=3)
    # refresh_expires = timedelta(days=1)

    @staticmethod
    def json_serial(obj: datetime) -> str:
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError("Type %s not serializable" % type(obj))

    def encode_token(self, sub: Union[int, str], expires: timedelta) -> str:
        """
        sub (subject) : 토큰의 주제를 나타내는 클레임입니다.
        iat (issued at) : 토큰 발급 시간
        exp (expires at) : 토큰 만료 시간

        나중에 r/w 권한도 넣어야하는 경우
        scope: read write
        """

        convert_expires = self.json_serial(get_kst_now() + expires)
        convert_iat = self.json_serial(get_kst_now())

        payload = {
            "exp": convert_expires,
            "iat": convert_iat,
            "sub": sub,
        }

        signed = jws.sign(payload, self.secret, algorithm=self.algorithm)

        return signed

    def decode_token(self, token: str) -> dict:
        try:
            decode_token = jws.verify(
                token, self.secret, algorithms=[self.algorithm]
            ).decode()
            payload = ast.literal_eval(decode_token)
            return payload

        except jws.JWSSignatureError:
            raise TokenExceptions.TokenExpired
        except jws.JWSError:
            raise TokenExceptions.InvalidToken

    def create_access_token(self, user_id: int) -> str:
        """
        user id만 sub으로 담음
        sub는 decode를 통해 인증/인가에 사용
        """
        sub = user_id
        return self.encode_token(sub, self.access_expires)

    def create_refresh_token(self, user_id: int) -> str:
        """
        리프레시 토큰으로 인증/인가를 할 수 없도록 액세스 토큰과 다른 sub내용 생성
        sub : user_id + 'refresh'
        """
        sub = f"{user_id}.refresh"
        return self.encode_token(sub, self.refresh_expires)

    def create_jwt_token(self, user_id: int) -> tuple:

        access_token = self.create_access_token(user_id)
        refresh_token = self.create_refresh_token(user_id)

        db = database.SessionLocal()
        try:
            access_model = JWTAccessToken(
                user_id=user_id,
                token=access_token,
            )
            refresh_model = JWTRefreshToken(
                access_token=access_model,
                token=refresh_token,
            )
            db.add(access_model)
            db.add(refresh_model)
            db.commit()

        except Exception:
            db.rollback()
            raise FailedCreateToken
        finally:
            db.close()

        return access_token, refresh_token

    @staticmethod
    def revoke_jwt_token(input_data: JWTTokenRequest) -> bool:

        access_token = input_data.access_token
        refresh_token = input_data.refresh_token

        db = database.SessionLocal()
        try:
            access_token = (
                db.query(JWTAccessToken).filter_by(token=access_token).first()
            )

            refresh_token = (
                db.query(JWTRefreshToken).filter_by(token=refresh_token).last()
            )
            now = get_kst_now()

            refresh_token.revoked = now
            db.delete(access_token)
            db.commit()

        except Exception:
            db.rollback()
            raise FailedLogOUt
        finally:
            db.close()

        return True
