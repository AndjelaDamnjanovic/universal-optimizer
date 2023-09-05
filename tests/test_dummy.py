from pathlib import Path
directory = Path(__file__).resolve()
import sys
sys.path.append(directory.parent)

import unittest   
import unittest.mock as mock

class TestDummy(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("setUpClass\n")

    def setUp(self):
        self.dummy_val = 42

        self.dummy_obj = mock.MagicMock()
        type(self.dummy_obj).name = mock.PropertyMock(return_value='some_problem')
        type(self.dummy_obj).dimension = mock.PropertyMock(return_value=42)
        return
    
    def test_dummy_obj_name_should_be_some_problem(self):
        self.assertEqual(self.dummy_obj.name, 'some_problem')

    def test_dummy_obj_dimension_should_be_42(self):
        self.assertEqual(self.dummy_obj.dimension, 42)

    def test_dummy_obj_dimension_should_be_dummy_val(self):
        self.assertEqual(self.dummy_obj.dimension, self.dummy_val)

    def tearDown(self):
        return

    @classmethod
    def tearDownClass(cls):
        print("\ntearDownClass")
    
if __name__ == '__main__':
    unittest.main()