import os
import io
import uuid
import json
from azure.storage.blob import BlockBlobService, PublicAccess

class Blob():

    def __init__(self, container_name='smartbin'):
        
        self.blob_service = BlockBlobService(account_name = 'iotinfstore', account_key = 'VxbwD/Cjvfi+ZObPIkqZ7AT8NKG3AqF6m0jYEUiwU12xtpiotyxIRNRyKu208P1+W+DdYKZd0SzFii2SrcsgWQ==') 

        self.container_name = container_name

    def write_data_to_blob(self,data):
        
        self.blob_service.create_blob_from_text(self.container_name, str(uuid.uuid4()), data)
        # self.blob_service.create_blob_from_text(self.container_name, "charly", data)
    
