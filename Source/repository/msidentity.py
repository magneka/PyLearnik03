import base64
import hashlib
import codecs
from  base64 import b64decode
from random import randbytes

# =============================================================================
# Klasse for ms_identity   
# =============================================================================

class ms_identity:
    _default_iterations: None
    _default_saltlen: None
    _default_identity_version: None
    _default_hash_algorithm: None
    
    def __init__(self):
        self._default_identity_version = 1
        self._default_iterations = 10000
        self._default_saltlen = 16
        self._default_hash_algorithm = 1 # PBKDF2WithHmacSHA256
        
    def check_password(self, password: str, identity_record: str) -> bool:
        
        # Konverterer passordet til byte array
        password_bytes = bytes(password, "utf-8")

        # Decode the identity record, den er base64 kodet så den kan lagres som en ascii string
        identity_decoded = b64decode(identity_record)
    
        # Identity version 0 or 1 Expected 1
        p1_1 = identity_decoded[0:1]
        identity_version = int.from_bytes(p1_1, "little")
        
        # Hash algorithm version, expected 1 (0=SHA1, 1=SHA256, 2=SHA512 )
        p2_5 = identity_decoded[1:5]
        hash_algorithm_version = int.from_bytes(p2_5, "big")
        hashalgorithm_name = self.getHashAlgorithmAsString(hash_algorithm_version)
        
        # Number of iterations    
        p6_9 = identity_decoded[5:9]
        iterations = int.from_bytes(p6_9, "big")
        
        # Length of salt string (Expected 16)
        p10_13 = identity_decoded[9:13]
        saltsize = int.from_bytes(p10_13, "big")

        # Actual salt string (16 characters)
        p14_29 = identity_decoded[13:29]
        
        # The result we should have...
        p30_61 = identity_decoded[29:61]
            
        salt_bytes = p14_29          
        subkeySize = 32    
        
        if hashalgorithm_name == 'PBKDF2WithHmacSHA256':
            actualSubkey = hashlib.pbkdf2_hmac('sha256', password_bytes, salt_bytes, iterations, subkeySize)
        elif hashalgorithm_name == 'SHA512':
            actualSubkey = hashlib.pbkdf2_hmac('sha512', password_bytes, salt_bytes, iterations, subkeySize)        
        else:
            return False

        ch_org:str = codecs.getencoder('hex_codec')(p30_61)[0] 
        ch_new:str = codecs.getencoder('hex_codec')(actualSubkey)[0] 
        
        return ch_org == ch_new
    
    def generate_identity_record(self, password: str) -> str:
        
        password_bytes = bytes(password, "utf-8")

        #a = 1
        identity_version_bytes = self._default_identity_version.to_bytes(1, 'little') 
        
        #a = 1 
        hash_algorithm_bytes = self._default_hash_algorithm.to_bytes(4, 'big') 
        
        iterations = self._default_iterations
        iterations_bytes = iterations.to_bytes(4, 'big') 
        
        #salt_length = 16
        salt_length_bytes = self._default_saltlen.to_bytes(4, 'big') 

        salt_bytes = randbytes(16)
        #salt_bytes = b'Qz\x91\xa5\x1fT[J\xbb\xc2nL:\xb9>\xeb'
        #tt = salt_string.decode("utf-8")

        subkeySize = 32        
        actualSubkey = None
        hashalgorithm_name = self.getHashAlgorithmAsString(self._default_hash_algorithm)
        if hashalgorithm_name == 'PBKDF2WithHmacSHA256':
            actualSubkey = hashlib.pbkdf2_hmac('sha256', password_bytes, salt_bytes, iterations, subkeySize)
        elif hashalgorithm_name == 'SHA512':
            actualSubkey = hashlib.pbkdf2_hmac('sha512', password_bytes, salt_bytes, iterations, subkeySize)
        else:
            return ""

        identity_as_bytes = identity_version_bytes + hash_algorithm_bytes + iterations_bytes + salt_length_bytes + salt_bytes + actualSubkey

        identity_base64_encoded = base64.b64encode(identity_as_bytes)
        #print(identity_base64_encoded)

        return identity_base64_encoded
        
    def getHashAlgorithmAsString (self, i:int) -> str:

        if i == 0:
            return "SHA1"
        elif i == 1:
            return "PBKDF2WithHmacSHA256"
        elif i == 2:
            return "SHA512"

        return ""