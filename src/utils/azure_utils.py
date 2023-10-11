from typing import AnyStr, Iterable, IO
import logging

from azure.core.exceptions import HttpResponseError
from azure.storage.blob import BlobServiceClient

logging.basicConfig(filename='azure_util.log',
                    level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')


class AzureStorage(object):
    def __init__(self,
                 account_name: str,
                 account_key: str,
                 ):
        self.account_name = account_name
        self.account_key = account_key
        self.blob_service_client = BlobServiceClient(account_url=f"https://{self.account_name}.blob.core.windows.net",
                                                     credential=self.account_key)

    def store(self,
              container_name: str,
              blob_name: str,
              data_to_store: bytes | str | Iterable[AnyStr] | IO[AnyStr],
              chunk_size=4 * 1024 * 1024) -> bool:

        global blob_client
        data_size = len(data_to_store)
        chunks = [data_to_store[i:i + chunk_size] for i in range(0, data_size, chunk_size)]
        max_retries = 3
        retries = 0
        try:
            logging.info(f'Start Storing at {container_name}....')
            container_client = self.blob_service_client.get_container_client(container_name)
            blob_client = container_client.get_blob_client(blob_name)
            blob_client.upload_blob(data_to_store, overwrite=True)
            logging.info(f'Storing operation completed!')
            return True
        except HttpResponseError as e:
            logging.exception(f'Initial upload attempt failed with error: {e}')
            while retries < max_retries:
                try:
                    for chunk in chunks:
                        blob_client.upload_blob(chunk, overwrite=False)
                    return True
                except HttpResponseError as e:
                    logging.exception(f'Upload attempt {retries + 1} failed with error: {e}')
                    retries += 1
            return False

    def delete(self,
               container_name: str,
               blob_name: str,
               ) -> bool:
        try:
            logging.info(f'Start Deleting blob at {blob_name}')
            container_client = self.blob_service_client.get_container_client(container_name)
            blob_client = container_client.get_blob_client(blob_name)
            blob_client.delete_blob()
            logging.info(f'Deletion Done!')
            return True
        except Exception as E:
            logging.exception(str(E))
            return False

    def list_all_blobs(self, container_name: str) -> list | None:
        blobs = []
        try:
            container_client = self.blob_service_client.get_container_client(container_name)
            for blob in container_client.list_blobs():
                blobs.append(blob)
            return blobs
        except Exception as E:
            logging.exception(str(E))
            return None

    def retrieve(self,
                 container_name: str,
                 blob_name: str,
                 ) -> bytes | None:
        try:
            logging.info(f'Start retrieving from Container: {container_name}, blob: {blob_name}')
            container_client = self.blob_service_client.get_container_client(container_name)
            blob_client = container_client.get_blob_client(blob_name)
            blob_data = blob_client.download_blob()
            data_bytes = blob_data.readall()
            logging.info(f'Retrival is done!')
            return data_bytes
        except Exception as E:
            logging.exception(str(E))
            return None


if __name__ == '__main__':
    pass
