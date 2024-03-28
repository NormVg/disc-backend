from tinydb import TinyDB
from tinydb import Query
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import eyed3
import gdown
import os

import config

gauth = GoogleAuth()
gauth.LoadClientConfigFile(config.client_config)
gauth.LoadCredentialsFile(config.cred)
drive = GoogleDrive(gauth)

audio = TinyDB(config.audio_db)
playlist = TinyDB(config.playlist_db)
folder = TinyDB(config.folder_db)
fQ = Query()


def get_album_art(id):

    name = config.temp_audio
    if f"{id}.png" in os.listdir(config.art_dir):
        print("art allready there")
        return f"{config.art_dir}/{id}.png"
    
    if f"{id}.jpg" in os.listdir(config.art_dir):
        return f"{config.art_dir}/{id}.jpg"
    
    gdown.download(id=id,output=name)
    file = name
    audiofile = eyed3.load(file)
    
    try:
        if audiofile.tag.images:
            for image in audiofile.tag.images:
                art = f"{config.art_dir}/{id}.{image.mime_type.split('/')[1]}"
                with open(art, "wb") as img_file:
                    img_file.write(image.image_data)
                    img_file.close()
                return art
                
        else:
            return config.common_art
    except: return config.common_art


def get_file_list(parent):
    file_list = drive.ListFile({'q': f"'{parent}' in parents and trashed=false"}).GetList()
    return file_list

catgry = {"hiphop":"1f7V7JZ3_JJRCerPZ29ympK592A-hltla","hindi":"1aAxMnwdvrPuElQRKKjxg-D13LO_PWVx7","english":"16RHi1_BKPf9Cna-F5P8_ScpeR4xcWOfU"}

def audio_update(name,id,cat,art): 
    data =  {
    "name":name,
    "id":id,
    "catg":cat,
    "artist":art,
    "art":f"/api/album-art?id={id}"
    }
    audio.insert(data)

def SyncDrive():
    audio.truncate()
    folder.truncate()
    print("syncing drive")
    for i in catgry.keys():
        songs_by_cat = []
        files = get_file_list(catgry.get(i))
        for k in files:
            if k['mimeType'] == "application/vnd.google-apps.folder":
                songs_by_art = []
                for g in get_file_list(k['id']):# songs with artist
                    name,id,cat,artist = g['title'],g['id'],i,k['title']
                    songs_by_art.append({"name":name,"id":id})
                    audio_update(name=name,id=id,cat=cat,art=artist)
                folder.insert({artist:songs_by_art,"id":k['id']})
            else:#songs without artist
                name,id,cat,artist = k['title'],k['id'],i,None
                audio_update(name=name,id=id,cat=cat,art=artist)
                songs_by_cat.append({"name":name,"id":id})
        folder.insert({i:songs_by_cat,"id":catgry.get(i)})
        
        
    print("drive is synced ")


# SyncDrive()

def get_artist_all():
    
    all_folder = folder.all()

    return all_folder

def audio_by_artist(id):
    return folder.search(fQ.id == id)
    


