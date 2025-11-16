from typing import List, Tuple
import unittest
from unittest.mock import patch, Mock
from regular import PhoneNumberExtractor


class TestPhoneNumberExtractor(unittest.TestCase):
    
    def setUp(self):
        self.extractor = PhoneNumberExtractor()