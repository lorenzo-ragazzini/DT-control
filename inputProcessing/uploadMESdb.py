# -*- coding: utf-8 -*-
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from time import sleep
import json

def donwload(path_to_file,timeout=1):
    while True:
        sleep(timeout)
        connection_string = 'DefaultEndpointsProtocol=https;AccountName=cloudformesdata;AccountKey=V3a7emh71+MSTdHykDKaZS9NPzwlp/orebGlYCNGNet5PgRgl7o94lafftuIO1JaOc+sNjFisdCt+AStR14uag==;EndpointSuffix=core.windows.net'
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_name = 'test'
        blob_name = 'MESb.xlsx'
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        local_file_path = 'a.pdf'
        with open(local_file_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
        print(f'File {blob_name} downloaded from {container_name}.')

def upload(timeout=1):
    while True:
        sleep(timeout)
        connection_string = 'DefaultEndpointsProtocol=https;AccountName=cloudformesdata;AccountKey=V3a7emh71+MSTdHykDKaZS9NPzwlp/orebGlYCNGNet5PgRgl7o94lafftuIO1JaOc+sNjFisdCt+AStR14uag==;EndpointSuffix=core.windows.net'
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_name = 'test'
        blob_name = 'test'
        container_client = blob_service_client.get_container_client(container_name)
        try:
            container_client.get_blob_client(blob_name).delete_blob()
        except:
            pass
        with open('D://a.pdf', 'rb') as data:
            container_client.upload_blob(name=blob_name, data=data)
        print(f'File {blob_name} uploaded to {container_name}.')

def setToModel():
    pass

with open('config.json') as f:
    paths = json.load(f)
    input_path = paths['input_path']
    filename = 'prova.xlsx'
    path_to_file = input_path + filename
donwload(path_to_file,timeout=1)