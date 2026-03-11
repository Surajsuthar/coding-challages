import os
import unittest

from lib.lexer import Lexer
from lib.syntax import Syntax


class TestJSONParser(unittest.TestCase):
    """Unit tests for JSON parser using existing test files"""

    def setUp(self):
        self.lexer = Lexer()
        self.test_dir = os.path.dirname(os.path.abspath(__file__))

    def parse_json_file(self, filepath):
        """Parse a JSON file and return the result"""
        with open(filepath, 'r') as f:
            content = f.read()
        tokens = self.lexer.tokenize(content)
        syntax = Syntax(tokens=tokens, index=0)
        return syntax.parse()

    def test_step1_valid_empty_object(self):
        """Test step 1: Parse valid empty object"""
        result = self.parse_json_file(os.path.join(self.test_dir, 'test/step1/valid.json'))
        self.assertEqual(result, {})

    def test_step1_invalid_file(self):
        """Test step 1: Invalid JSON should raise an exception"""
        with self.assertRaises(Exception):
            self.parse_json_file(os.path.join(self.test_dir, 'test/step1/invalid.json'))

    def test_step2_valid_simple_object(self):
        """Test step 2: Parse valid object with string key-value"""
        result = self.parse_json_file(os.path.join(self.test_dir, 'test/step2/valid.json'))
        self.assertEqual(result, {"key": "value"})



    def test_step2_invalid2(self):
        """Test step 2: Invalid JSON should raise exception"""
        with self.assertRaises(Exception):
            self.parse_json_file(os.path.join(self.test_dir, 'test/step2/invalid2.json'))

    def test_step2_invalid3(self):
        """Test step 2: Invalid JSON should raise exception"""
        with self.assertRaises(Exception):
            self.parse_json_file(os.path.join(self.test_dir, 'test/step2/invalid3.json'))

    def test_step3_valid_all_types(self):
        """Test step 3: Parse object with multiple value types"""
        result = self.parse_json_file(os.path.join(self.test_dir, 'test/step3/valid.json'))
        self.assertEqual(result["key1"], True)
        self.assertEqual(result["key2"], False)
        self.assertIsNone(result["key3"])
        self.assertEqual(result["key4"], "value")
        self.assertEqual(result["key5"], 101)

    def test_step3_invalid_file(self):
        """Test step 3: Invalid JSON should raise exception"""
        with self.assertRaises(Exception):
            self.parse_json_file(os.path.join(self.test_dir, 'test/step3/invalid.json'))

    def test_step4_invalid_file(self):
        """Test step 4: Invalid JSON should raise exception"""
        with self.assertRaises(Exception):
            self.parse_json_file(os.path.join(self.test_dir, 'test/step4/invalid.json'))

    def test_step5_invalid_file(self):
        """Test step 5: Invalid JSON should raise exception"""
        with self.assertRaises(Exception):
            self.parse_json_file(os.path.join(self.test_dir, 'test/step5/invalid.json'))


if __name__ == '__main__':
    unittest.main()
