from datetime import datetime, timezone, timedelta
import jwt

# =============================================================================
# Klasse for jwt_token   
# =============================================================================


class jwt_token:
    _secret: None
    
    def __init__(self):
        self._secret = "TESTSECRET"
        self._issuer = "https://example.com"
        self._audience = "https://example.com"
        self._algorithm = "HS256"
        self._expiration_time = 3600
        
    def get_jwt_token(self, username: str) -> str:
        encoded = jwt.encode(
            {"user": username,
             "aud": self._audience,
             "iss": self._issuer,
             "iat": datetime.now(tz=timezone.utc),
             "exp":datetime.now(tz=timezone.utc) + timedelta(seconds=self._expiration_time)}, 
            self._secret, 
            algorithm=self._algorithm,            
        )
        return encoded
    
    def decode_jwt_token(self, token: str) -> dict:
        decoded = jwt.decode(token, self._secret, algorithms=[self._algorithm], audience=self._audience, issuer=self._issuer)
        return decoded
    
    def validate_jwt_token(self, token: str) -> bool:
        try:
            decoded = jwt.decode(token, self._secret, algorithms=[self._algorithm], audience=self._audience, issuer=self._issuer)
            return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
        
    # def get_jwt_token_from_request(self, request) -> str:   
    #     auth_header = request.headers.get("Authorization")
    #     if auth_header:
    #         token = auth_header.split(" ")[1]
    #         return token
    #     return None