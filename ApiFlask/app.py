from flask import Flask, jsonify, request, render_template, json
from flask_ngrok import run_with_ngrok
from werkzeug.utils import secure_filename
from db import db_init, db
from models import Img
import cv2
import os
import numpy as np
import io
# method = 'EigenFaces'
# method = 'FisherFaces'


app = Flask(__name__)
run_with_ngrok(app) 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///img.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)


#method = 'EigenFaces'
method = 'FisherFaces'
#method = 'LBPH'

if method == 'EigenFaces': emotion_recognizer = cv2.face.EigenFaceRecognizer_create()
if method == 'FisherFaces': emotion_recognizer = cv2.face.FisherFaceRecognizer_create()
if method == 'LBPH': emotion_recognizer = cv2.face.LBPHFaceRecognizer_create()
emotion_recognizer.read('modelo'+method+'.xml')
dataPath = 'C:/Users/Usuario/Desktop/Proyecto/data/'
imagePath = os.listdir(dataPath)
faceClassif = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "pong!"})




@app.route('/archivo', methods=['POST'])
def upload():

    pic = request.files['pic']
    pic2= request.files['pic2']
    if not pic:
        return 'No archivo', 400
    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    #img = Img(img=pic.read(), mimetype=mimetype, name=filename)
    #db.session.add(img)
    #db.session.commit()

    #read image file string data
    npimg = np.fromfile(pic, np.uint8)
    # convert numpy array to image
    gray1 = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(gray1, cv2.COLOR_BGR2GRAY)
   
    #gray = cv2.imdecode(imgcv2, cv2.COLOR_BGR2GRAY)

    auxFrame = gray.copy()
    faces = faceClassif.detectMultiScale(gray, 1.3, 5)
    print(faces)
  
    for (x, y, w, h) in faces:
        rostro = auxFrame[y:y+h, x:x+w]
        rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
        result = emotion_recognizer.predict(rostro)
        if method == 'LBPH':
            if result[1] < 70:
                  img = Img(img=pic2.read(), mimetype=mimetype, name=filename)
                  db.session.add(img)
                  db.session.commit()
                  return jsonify({"Emocion": imagePath[result[0]],"Error":False,"Errormsg":""})
 				# image = emotionImage(imagePath[result[0]])
 				# nFrame = cv2.hconcat([frame,image3])
            else:
                  img = Img(img=pic2.read(), mimetype=mimetype, name=filename)
                  db.session.add(img)
                  db.session.commit()
                  return jsonify({"Emocion": "","Error":True,"Errormsg":"Emocion desconcida"})                                     
 				# nFrame = cv2.hconcat([frame,np.zeros((480,300,3),dtype=np.uint8)])
        if method == 'FisherFaces':
            if result[1] < 500:
                  img = Img(img=pic2.read(), mimetype=mimetype, name=filename)
                  db.session.add(img)
                  db.session.commit()
                  return jsonify({"Emocion": imagePath[result[0]],"Error":False,"Errormsg":""})
 				# image = emotionImage(imagePath[result[0]])
 				# nFrame = cv2.hconcat([frame,image3])
            else:
                  img = Img(img=pic2.read(), mimetype=mimetype, name=filename)
                  db.session.add(img)
                  db.session.commit()
                  return jsonify({"Emocion": "","Error":True,"Errormsg":"Emocion desconcida"})                                     

        if method == 'EigenFaces':
            if result[1] < 5700:
                  img = Img(img=pic2.read(), mimetype=mimetype, name=filename)
                  db.session.add(img)
                  db.session.commit()
                  return jsonify({"Emocion": imagePath[result[0]],"Error":False,"Errormsg":""})
 				# image = emotionImage(imagePath[result[0]])
 				# nFrame = cv2.hconcat([frame,image3])
            else:
                  img = Img(img=pic2.read(), mimetype=mimetype, name=filename)
                  db.session.add(img)
                  db.session.commit()
                  return jsonify({"Emocion": "","Error":True,"Errormsg":"Emocion desconcida"})                                     
    # print(pic.read())
    return jsonify({"Emocion": "","Error":True,"Errormsg":"No se encontro ningun rostro"})

if __name__ == '__main__':
    #app.run(debug=True, host='192.168.100.242' ,port=80)
    app.run()
