import unittest

# Create your tests here.
from .fields import TrimpCharField

class TestTrimpCharField(unittest.TestCase):
    def test_to_python(self):
        value = '   hello   '
        expected_output = 'hello'
        field = TrimpCharField(max_length=50)

        self.assertEqual(field.to_python(value), expected_output)