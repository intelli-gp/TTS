from ....src.utils.azure_utils import AzureStorage
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from datetime import datetime
class AzureStorageSas(AzureStorage):

    def __init__(self,acc_name,acc_key,container_name):
        AzureStorage.__init__(self, acc_name,acc_key)
        self.container_name = container_name

    def store_blob(self,video_name,video_path):
        blob_name = datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + video_name
        self.store(self.container_name,blob_name,video_path)
        return blob_name


    def get_blob_sas(self,container_name, blob_name):
        sas_blob = generate_blob_sas(account_name=self.azure_storage_object.acc_name, 
                                    container_name=container_name,
                                    blob_name=blob_name,
                                    account_key=self.azure_storage_object.acc_key,
                                    permission=BlobSasPermissions(read=True),
                                    expiry=datetime.utcnow() + timedelta(hours=1))
        return sas_blob