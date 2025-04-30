import unittest

from msidentity import ms_identity


class ucIdentityTests(unittest.TestCase):
    
    msidentity = None
    
    def setUp(self):
        self.msidentity = ms_identity()
        
    def test_check_password(self):        
        password = "Test123!"
        identity_record = 'AQAAAAEAACcQAAAAEFF6kaUfVFtKu8JuTDq5PuuBXLGFIdrLCqUGivmyNiyQfn3WGCWBcr9wtSwJ9A1E7A=='
        res = self.msidentity.check_password(password, identity_record)
        self.assertTrue(res, "Password check failed")
        
    def test_check_invalid_password(self):        
        password = "Test123?"
        identity_record = 'AQAAAAEAACcQAAAAEFF6kaUfVFtKu8JuTDq5PuuBXLGFIdrLCqUGivmyNiyQfn3WGCWBcr9wtSwJ9A1E7A=='
        res = self.msidentity.check_password(password, identity_record)
        self.assertFalse(res, "Password should fail")
        
    def test_generate_identity_record(self):
        password = "Test123!"
        identity_record = self.msidentity.generate_identity_record(password)     
        
        chk = self.msidentity.check_password(password, identity_record)   
        self.assertTrue(chk, "Password check failed")
        self.assertTrue(identity_record != "", "Identity record generation failed")
        
    def test_generate_identity_record_fail(self):
        password = "Test123!"
        identity_record = self.msidentity.generate_identity_record(password)     
        
        password = "Test123?"
        chk = self.msidentity.check_password(password, identity_record)   
        self.assertFalse(chk, "Password should failed")
        self.assertTrue(identity_record != "", "Identity record generation failed")
        
    def test_generate_identity_record_sha512(self):
        msidentity = ms_identity()
        msidentity._default_hash_algorithm = 2 # SHA512
        password = "Test123!"
        
        identity_record = msidentity.generate_identity_record(password)             
        chk = self.msidentity.check_password(password, identity_record)   
        
        self.assertTrue(chk, "Password check failed")
        self.assertTrue(identity_record != "", "Identity record generation failed")
        
    def test_generate_identity_record_sha512_2(self):
        msidentity = ms_identity()
        msidentity._default_hash_algorithm = 2 # SHA512
        msidentity._default_iterations = 1000000 # Better hashing and longer time
        password = "Test123!"
        
        identity_record = msidentity.generate_identity_record(password)             
        chk = self.msidentity.check_password(password, identity_record)   
        
        self.assertTrue(chk, "Password check failed")
        self.assertTrue(identity_record != "", "Identity record generation failed")
        
    
if __name__ == '__main__':
    unittest.main()