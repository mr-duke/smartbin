import os
import io
import uuid
import json
from azure.storage.blob import BlockBlobService, PublicAccess

class Blob():

    def __init__(self, container_name='smartbin'):
        
        self.blob_service = BlockBlobService(account_name = 'iotinfstore', account_key = 'VxbwD/Cjvfi+ZObPIkqZ7AT8NKG3AqF6m0jYEUiwU12xtpiotyxIRNRyKu208P1+W+DdYKZd0SzFii2SrcsgWQ==') 

        self.container_name = container_name

        #self.blob_service.create_container(container_name) 
        # Set the permission so the blobs are public.
        #self.blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)

    
    def write_data_to_blob(self,data):
        
        self.blob_service.create_blob_from_text(self.container_name, str(uuid.uuid4()), data)
    

# Main
if __name__ == '__main__':
    try:
        blob = Blob()
        blob.write_data_to_blob(json.dumps({'DeviceId': str(uuid.uuid1()),'Temp': 12.1}))
        #blob.list_blob_content()

    except Exception as e:
        print("Top level Error: args:{0}, message:N/A".format(e.args))
