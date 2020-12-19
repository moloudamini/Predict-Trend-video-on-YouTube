import unittest
from maintest import *

class Test_function_youtube(unittest.TestCase):
    def test_import_rows_accuracy(self):
        tablename = 'Views_CA'
        actual_rows, isCorrect = check_import_accuracy(tablename,58881)
        self.assertEqual(actual_rows, 58881)
        self.assertEqual(isCorrect, 'correct')
        
    def test_rows_columns_accuracy(self):
        tablename = 'Views_CA'
        isCorrect, actual_rows, actual_cols = check_row_columns_accuracy(tablename,58881,8)
        self.assertEqual(isCorrect, 'correct rows and columns')
        self.assertEqual(actual_rows, 58881)
        self.assertEqual(actual_cols, 8)

    def test_rows_columns_accuracy2(self):
        tablename = 'Views_CA'
        expected_rows = count_num_records(tablename)
        expected_cols = count_num_columns (tablename)
        isCorrect, actual_rows, actual_cols = check_row_columns_accuracy(tablename, expected_rows, expected_cols)
        self.assertEqual(isCorrect, 'correct rows and columns')
        self.assertEqual(actual_rows, expected_rows)
        self.assertEqual(actual_cols, expected_cols)

    def test_num_csv_rows(self):
        filename = 'CAviews.csv'
        results = count_csv_file_records(filename)
        self.assertEqual(results, 40882)

    def test_num_table_rows(self):
        tablename = 'Views_CA'
        results = count_num_records(tablename)
        self.assertEqual(results, 58881)

    def test_num_table_cols(self):
        tablename = 'Views_CA'
        results = count_num_columns(tablename)
        self.assertEqual(results, 8)


if __name__ == '__main__':
    unittest.main()

