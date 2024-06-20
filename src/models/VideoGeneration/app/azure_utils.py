import logging
from azure.storage.blob import BlobServiceClient, BlobType, ContentSettings, BlobClient, BlobBlock

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
              data_to_store_path: str,
              chunk_size: int = 1024 * 1024 * 4) -> bool:
        import uuid
        """
        @Description:
        :arg
            container_name: the exist container in the storage account 
            blob_name:      name of the file that will be stored in the given container 
            data_to_store_path: local path of the file that you want to upload
            chunk_size: chunk size to upload the file by default 4MB
                        this function depends mainly on the upload speed ,if it was not suitable and give timeout 
                        you can change the chunk size to be less than 4MB for ex. 1MB -> 1024*1024*1
        :return
            bool: status of the operation True -> success , False -> failure 
        """
        try:
            container_client = self.blob_service_client.get_container_client(container_name)
            blob_client = container_client.get_blob_client(blob_name)
            # upload data
            block_list = []

            with open(data_to_store_path, 'rb') as f:
                while True:
                    read_data = f.read(chunk_size)
                    if not read_data:
                        break  # done
                    blk_id = str(uuid.uuid4())
                    blob_client.stage_block(block_id=blk_id, data=read_data)
                    block_list.append(BlobBlock(block_id=blk_id))
            blob_client.commit_block_list(block_list)
            return True
        except BaseException as err:
            logging.exception(err)
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

    def list_all_blobs(self, container_name: str) -> list:
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
                 ) -> bytes:
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
