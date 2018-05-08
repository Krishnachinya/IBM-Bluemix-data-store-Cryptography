import swiftclient
from keystoneclient import client
import re
import os
import sys
import base64

#Basic connection details
auth_url= "https://identity.open.softlayer.com/v3"
project=""
projectId="cf44dcfa4d8348228bd1e34628782152"
region="london"
userId="f9edee1918a94adfbd76468f10b99b32"
username=""
password="RkTzL4,8eqsI3y(]"

container_name = 'prjcld_chinya'
Uploadpath = '/Users/KrishnChinya/Desktop/Bluemix'
Downloadpath = '/Users/KrishnChinya/Desktop/Bluemix_download'
extension = ['txt','Txt','pdf','PDF','PNG','png','html','jpg']

connectionst = swiftclient.Connection(authurl=auth_url,key=password,auth_version='3',os_options={"project_id": projectId,\
                                    "user_id": userId,"region_name": region})

x = connectionst.get_account()[1]

#[{u'count': 0, u'bytes': 0, u'name': u'prjcld_chinya'}]
#print x


# List your containers present in cloud
#print ("nContainer List:")
#for container in  connectionst.get_account()[1]:
#	print container['name']

try:
    for (dirpath,dirnames,filenames) in os.walk(Uploadpath):
        for fl in filenames:
            if fl.endswith(tuple(extension)):
                print fl
                with open(dirpath +'/' + fl, 'r') as file:
                    base64_encode = base64.encodestring(file.read())
                    connectionst.put_object(container_name,fl,contents=base64_encode,content_type='text')
                    file.close()
                    #copy_object(container_name,)
except:
    print("Unexpected error:", sys.exc_info()[0])

print x

#list all the files in the container
print("number of files are")
print("FileName \t\t\t Last Modified \t\t\t\t Bytes \t Content Type")
for container in connectionst.get_account()[1]:
    for datafiles in connectionst.get_container(container['name'])[1]:
        print "%s \t %s \t %s \t %s \t" %(datafiles['name'].strip(), datafiles['last_modified'].strip(),\
                                          datafiles['bytes'],datafiles['content_type'])
        #to download file
        download = connectionst.get_object(container['name'],datafiles['name'])
        with open(Downloadpath +'/'+ datafiles['name'],'w') as download_file:
            base64_decode = base64.decodestring(download[1])
            download_file.write(base64_decode)
            download_file.close()

#delete file

print ("delete one file")
connectionst.delete_object(container_name, "Krishna.jpg")