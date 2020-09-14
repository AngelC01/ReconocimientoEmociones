import cv2
import os
import numpy as np
import time

def obterner(method, facesData, labels):
	if method == 'EigenFaces': emotion_recognizer = cv2.face.EigenFaceRecognizer_create()
	if method == 'FisherFaces': emotion_recognizer = cv2.face.FisherFaceRecognizer_create()
	if method == 'LBPH': emotion_recognizer = cv2.face.LBPHFaceRecognizer_create()

	#Aqui esta entrenando c:
	print('Entrenando('<method>')...')
	inicio = time.time()
	emotion_recognizer.train(facesData, np.array(labels))
	tiempoTrain = time.time() - inicio
	print('Tiempo de entrenamiento('+method+'):', tiempoTrain)

	#Almacenara el modelo obtenido
	emotion_recognizer.write('modelo'+method+'.xml')

dataPath = 'C:/Users/Usuario/Desktop/Proyecto/data/'
emocionList = os.listdir(dataPath)
print('Lista de personas: ', emocionList)

labels = []
facesData = []
label = 0

for nameDir in emocionList:
	emocionPath = dataPath + '/' + nameDir
	print('Leyendo las imagenes')

	for fileName in os.listdir(emocionPath):
		print('Rostros', nameDir + '/' + fileName)
		labels.append(label)
		facesData.append(cv2.imread(emocionPath + '/' + fileName,0))
		#image = cv2.imread(emocionPath + '/' + fileName, 0)

	label = label + 1

	
obterner('LBPH', facesData, labels)
obterner('FisherFaces', facesData, labels)
obterner('EigenFaces', facesData, labels)

