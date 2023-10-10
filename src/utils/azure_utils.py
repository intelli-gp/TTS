from azure.storage.blob import BlobServiceClient


# def store_to_blob():
#     # Replace with your Azure Storage account name and access key
#     account_name = 'graduationwork3664469496'
#     account_key = 'Vs7mgSGdtSV9S7c+CU8iRoFW74/QbqhHtsQuSudKKdE5sRsiU0k94vjFwOIlxRS79v0EsBxvQP0z+AStsanD+Q=='
#
#     # Create a BlockBlobService client
#     blob_service = BlobServiceClient(account_name=account_name, account_key=account_key)
#
#     # Specify the container and blob name
#     container_name = 'test-data-storage'
#     blob_name = 'from-colab'
#
#     # Specify the data you want to upload
#     data_to_upload = b'Hello, Azure Blob Storage!'
#
#     # Upload the data to the specified blob
#     blob_service.create_blob_from_bytes(container_name, blob_name, data_to_upload)
#
#     print(f'Data uploaded to blob: {blob_name} in container: {container_name}')


def store_blob_v2():
    # from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

    # Replace with your Azure Storage account name and access key
    account_name = 'graduationwork3664469496'
    account_key = 'Vs7mgSGdtSV9S7c+CU8iRoFW74/QbqhHtsQuSudKKdE5sRsiU0k94vjFwOIlxRS79v0EsBxvQP0z+AStsanD+Q=='


    # Create a BlobServiceClient
    blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net",
                                            credential=account_key)

    # Specify the container name
    container_name = 'test-data-storage'

    # Specify the blob name
    blob_name = 'from-local'

    # Specify the data you want to upload
    data_to_upload = b'Hello, Azure Blob Storage!'

    # Get a reference to the container
    container_client = blob_service_client.get_container_client(container_name)

    # Upload the data to the specified blob
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(data_to_upload, overwrite=True)

    print(f'Data uploaded to blob: {blob_name} in container: {container_name}')


if __name__ == '__main__':
    store_blob_v2()