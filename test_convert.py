import unittest
import pandas as pd
from convert import convert

INPUT_FILENAME = 'input-statements.psv'
EXPECTED_OUTPUT_FILENAME = 'expected-sessions.psv'
OUTPUT_FILENAME = 'output-sessions.psv'

class TestConvert(unittest.TestCase):

    def test_convert(self):
        convert(INPUT_FILENAME, OUTPUT_FILENAME)
        
        
        with open(OUTPUT_FILENAME, 'r') as file1:
            with open(EXPECTED_OUTPUT_FILENAME, 'r') as file2:
                difference = set(file1).difference(file2)
        difference.discard('\n')
        
        self.assertFalse(difference)
        
        
if __name__ == '__main__':
    unittest.main()