import unittest,sys,os
from src.utils.azure_utils import AzureStorage


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.azure_object = AzureStorage(
            account_name='graduationwork3664469496',
            account_key='!!!!screte-key!!!!'
        )

    def test_store_data(self):
        data_to_store = b"Hello, Azure Blob Storage!"
        status1 = self.azure_object.store(
            container_name='container1',
            blob_name='blob1',
            data_to_store=data_to_store)  # container doesn't exists

        self.assertEqual(status1, False)
        status2 = self.azure_object.store(
            container_name='test-data-storage',
            blob_name='test.txt',
            data_to_store=data_to_store
        )
        self.assertEqual(status2, True)

        status3 = self.azure_object.store(
            container_name='test-data-storage',
            blob_name='raw/test.txt',
            data_to_store=data_to_store
        )
        self.assertEqual(status3, True)

    def test_list_all_blobs(self):
        pass

    def test_delete(self):
        pass

    def test_retrieve(self):
        pass


if __name__ == '__main__':
    unittest.main()
