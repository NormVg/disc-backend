from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pprint import pprint
import os
gauth = GoogleAuth()
gauth.LoadCredentialsFile("cred.json")

# gauth.SaveCredentialsFile("cred.json")
drive = GoogleDrive(gauth)

def get_file_list():
    file_list = drive.ListFile({'q': "'1f7V7JZ3_JJRCerPZ29ympK592A-hltla' in parents and trashed=false"}).GetList()
    return file_list

print(get_file_list())

# replace `root` with ID of a drive or directory and give service account access to it
# fs = GDriveFileSystem("root", client_id=my_id, client_secret=my_secret)

# for root, dnames, fnames in fs.walk("root"):
#     ...
