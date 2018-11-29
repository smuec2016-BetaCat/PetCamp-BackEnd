from config import SECRET_KEY
from models.base import db
from passlib.apps import custom_app_context
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadSignature


class User(db.Model):
    """
    The model of user and authorization information
    """
    id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True, unique=True)
    username = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)

    def hash_password(self, password):
        """
        Save the hash password
        :param password: origin password
        """
        self.password_hash = custom_app_context.hash(str(password))

    def verify_password(self, password):
        """
        Verify the password
        :param password: origin password
        :return: bool
        """
        return custom_app_context.verify(password, self.password_hash)

    def generate_token(self, expiration=600):
        """
        Generate a new token
        :param expiration: how long it lasts
        :return: the signature
        """
        serializer = TimedJSONWebSignatureSerializer(SECRET_KEY, expiration)
        return serializer.dumps({"id": self.id}).decode("utf-8")

    @staticmethod
    def verify_token(token):
        """
        Verify the token
        :param token: the given signature
        :return: the user information or error message
        """
        serializer = TimedJSONWebSignatureSerializer(SECRET_KEY)
        try:
            data = serializer.loads(bytes(token, encoding="utf-8"))
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        return User.query.get(data["id"])
