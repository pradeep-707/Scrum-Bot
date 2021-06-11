import os
import jwt
from datetime import datetime


# generate a jwt with the given data
def generateJwt(data):
    try:
        algorithm = os.environ.get("JWT_ALGORITHM")
        jwtSecret = os.environ.get("JWT_SECRET")
        tokenExpireTime = int(os.environ.get("TOKEN_EXPIRE_TIME"))
        payload = data.copy()
        print("jwt algo:  ", algorithm)

        if tokenExpireTime != 0:
            payload["exp"] = datetime.now() + tokenExpireTime

        return jwt.encode(payload, jwtSecret, algorithm=algorithm)
    except Exception as e:
        print("Couldnt generate jwt", e)
        raise Exception(e)
        return ""