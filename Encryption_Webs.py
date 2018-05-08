from flask import Flask ,redirect, url_for, request,render_template
import swiftclient
from werkzeug.utils import secure_filename
import base64
import os

app = Flask(__name__)

@app.route('/Upload')
def upload():
    return render_template("Upload.html")

#Basic connection details
auth_url= "https://identity.open.softlayer.com/v3"
project=""
projectId="cf44dcfa4d8348228bd1e34628782152"
region="london"
userId="f9edee1918a94adfbd76468f10b99b32"
username=""
password="RkTzL4,8eqsI3y(]"

container_name = 'prjcld_chinya'
Uploadpath = '/Users/KrishnChinya/Desktop/Bluemix/web'
Downloadpath = '/Users/KrishnChinya/Desktop/Bluemix_download'
extension = ['txt','Txt','pdf','PDF','PNG','png','html','jpg']


connectionst = swiftclient.Connection(authurl=auth_url,key=password,auth_version='3',os_options={"project_id": projectId,\
                                    "user_id": userId,"region_name": region})




@app.route('/uploader',methods=['POST','GET'])
def uploader():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(Uploadpath, filename))
        for (dirpath, dirnames, filenames) in os.walk(Uploadpath):
            for fl in filenames:
                if fl.endswith(tuple(extension)):
                    print fl
                    with open(dirpath + '/' + fl, 'r') as file:
                        base64_encode = base64.encodestring(file.read())
                        connectionst.put_object(container_name, fl, contents=base64_encode, content_type='text')
                        file.close()
        return "File Uploaded Successfully to Cloud/Bluemix"

@app.route('/downloader')
def downloader():
    i = 0
    alldetails = {};
    for container in connectionst.get_account()[1]:
        for datafiles in connectionst.get_container(container['name'])[1]:
            alldetails[i] = datafiles['name']
            i = i+1;
            alldetails[i] = datafiles['last_modified']
            i = i + 1;
            alldetails[i] = datafiles['bytes']
            i = i + 1;
            alldetails[i] = datafiles['content_type']
            i = i + 1;

    print alldetails
    return render_template('Download.html', result=container_name , result2=alldetails)

@app.route('/downloadfile',methods=['POST','GET'])
def downloadfile():
    if request.method == 'POST':
        filename = request.form['filename']
        print filename
        # to download file
        download = connectionst.get_object(container_name, filename)
        print download
        with open(Downloadpath + '/' + filename, 'w') as download_file:
            base64_decode = base64.decodestring(download[1])
            download_file.write(base64_decode)
            download_file.close()
    return "File Downloaded Successfully to Cloud/Bluemix"

if __name__ == '__main__':
    app.run()

