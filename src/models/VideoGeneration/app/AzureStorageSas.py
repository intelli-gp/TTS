from azure_utils import AzureStorage
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
class AzureStorageSas(AzureStorage):

    def __init__(self,acc_name,acc_key,container_name):
        AzureStorage.__init__(self, acc_name,acc_key)
        self.container_name = container_name

    def get_blob_sas(self,container_name, blob_name):
        sas_blob = generate_blob_sas(account_name=self.account_name, 
                                    container_name=container_name,
                                    blob_name=blob_name,
                                    account_key=self.account_key,
                                    permission=BlobSasPermissions(read=True),
                                    expiry=datetime.utcnow() + timedelta(hours=1))
        return sas_blob