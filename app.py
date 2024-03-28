from flask import Flask,send_file,request,jsonify,redirect
from flask_cors import CORS
import manager


app = Flask(__name__)
CORS(app)

#api endpoints

@app.get("/api/album-art")
def album_art_api():
    id  = request.args.get("id")
    file = manager.get_album_art(id)
    return send_file(file)

@app.get("/api/audio")
def audio_files():
    id  = request.args.get("id")
    file = f"https://www.googleapis.com/drive/v3/files/{id}?alt=media&key=AIzaSyBUPpRFf2mdbDFgZ43YHfOsTpvf_Yg91Hc"
    return redirect(file)

@app.get("/api/all-audio")
def all_audio():
    a = manager.audio.all()
    return jsonify(a)

@app.get("/api/get-artist")
def get_artist():
    return jsonify(manager.get_artist_all())

@app.get("/api/audio-by-artist")
def by_artist():
    id = request.args.get("id")
    return jsonify(manager.audio_by_artist(id))



@app.get("/api/playlist-get")
def playlist_gen():
    tpe = request.args.get("type")
    id = request.args.get("id")
    if tpe  == "all": 
        manager.audio.all()
        return
    if tpe == "artist": 
        return
    if tpe == "playlist": 
        return

    return ""

@app.get("/api/sync")
def resync():
    manager.SyncDrive()
    return "Drive is synced now"



if __name__ == "__main__":
    app.run(debug=True,port=3333)