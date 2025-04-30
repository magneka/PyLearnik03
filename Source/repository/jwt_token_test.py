import unittest

from jwt_token import jwt_token


class ucIdentityTests(unittest.TestCase):
    
    _jwttoken = None
    
    def setUp(self):
        self._jwttoken = jwt_token()
        
    def test_check_password(self):        
        jwt_token = self._jwttoken.get_jwt_token("TestUser")
        print(f"JWT Token: {jwt_token}")              
    
if __name__ == '__main__':
    unittest.main()