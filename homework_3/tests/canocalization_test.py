import sys
sys.path.append("..")
import unittest
import Canonicalization 

class CanoTest(unittest.TestCase):
    def test_one(self):
        canoni = Canonicalization.Canonicalizer()
        
        result = canoni.canonicalize(
            "https://example.com/api/users",
            "/pages/1")
        
        self.assertEqual(result,"")
        
        
       
        
        