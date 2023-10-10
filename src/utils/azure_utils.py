from typing import AnyStr, Iterable, IO

from azure.storage.blob import BlobServiceClient


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
              data_to_store: bytes | str | Iterable[AnyStr] | IO[AnyStr]) -> bool:
        try:
            container_client = self.blob_service_client.get_container_client(container_name)
            blob_client = container_client.get_blob_client(blob_name)
            blob_client.upload_blob(data_to_store, overwrite=True)
            return True
        except Exception as E:
            print(str(E))
            return False

    def delete(self,
               container_name: str,
               blob_name: str,
               ) -> bool:
        try:
            container_client = self.blob_service_client.get_container_client(container_name)
            blob_client = container_client.get_blob_client(blob_name)
            blob_client.delete_blob()
            return True
        except Exception as E:
            print(str(E))
            return False

    def list_all_blobs(self, container_name):
        blobs = []
        container_client = self.blob_service_client.get_container_client(container_name)
        for blob in container_client.list_blobs():
            blobs.append(blob)
        return blobs

    def retrieve(self,
                 container_name: str,
                 blob_name: str,
                 ) -> bytes | None:
        try:
            container_client = self.blob_service_client.get_container_client(container_name)
            blob_client = container_client.get_blob_client(blob_name)
            blob_data = blob_client.download_blob()
            data_bytes = blob_data.readall()
            return data_bytes
        except Exception as E:
            print(str(E))
            return None





if __name__ == '__main__':
    pass

