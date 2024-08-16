import jwt
import datetime
from typing import Optional
import os, dotenv

dotenv.load_dotenv()

# Replace this with a strong secret key in production
SECRET_KEY = os.environ.get('jwt_secret')
ALGORITHM = "HS256"

# In-memory store for used tokens (this would be a database in production)

def create_jwt(email: str, address: str, expires_in_minutes: int = 5) -> str:
    """
    Create a JWT token with a specified expiration time.

    :param email: Email to include in the token.
    :param address: Ethereum address to include in the token.
    :param expires_in_minutes: Expiry time in minutes for the token.
    :return: Encoded JWT token as a string.
    """
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_in_minutes)
    payload = {
        "email": email,
        "address": address,
        "exp": expiration,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_jwt(token: str) -> Optional[dict]:
    print(token)
    """
    Decode a JWT token, ensuring it hasn't been used before.

    :param token: JWT token as a string.
    :return: Decoded payload as a dictionary if valid, None if already used.
    :raises jwt.ExpiredSignatureError: If the token has expired.
    :raises jwt.InvalidTokenError: If the token is invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        return payload

    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError("The token has expired")
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError("The token is invalid")


