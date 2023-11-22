
import unittest,sys,os
import base64
import unittest
from src.utils.azure_utils import AzureStorage


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.azure_object = AzureStorage(
            account_name='graduationwork3664469496',
            account_key='Vs7mgSGdtSV9S7c+CU8iRoFW74/QbqhHtsQuSudKKdE5sRsiU0k94vjFwOIlxRS79v0EsBxvQP0z+AStsanD+Q=='
        )

    def test_store_data(self):
        PATH_To_LARGE_FILE = "E:\\Downloads\\Compressed\\test.csv\\test.csv"

        status4 = self.azure_object.store(
            container_name='test-data-storage',
            blob_name='raw/test1.csv',
            data_to_store_path=PATH_To_LARGE_FILE
        )
        self.assertEqual(status4, True)

    def test_list_all_blobs(self):
        pass

    def test_delete(self):
        pass

    def test_retrieve(self):
        pass


if __name__ == '__main__':
    unittest.main()
