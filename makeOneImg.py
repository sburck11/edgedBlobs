from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import random
from blobClass.blob import Blob



			# shaderSigma=random.randint(25, 50)
			# blobThresh=random.randint(100, 120)
			# innerThresh=random.randint(70, 90)


# testImage=Blob(numBlob, minSize, maxSize, blobThresh, innerThresh,
			# sigma, shaderSigma, path, betweenBlobs, touchingEdge, flatBG, filterOn, addColors, name, hasEdges)
for i in range(50):
	numBlob=random.randrange(1,4)
	minSize=400
	maxSize=1000
	blobThresh=random.randint(110, 180)
	innerThresh=random.randint(5, 70)
	sigma=random.randint(50, 120)
	shaderSigma=random.randint(20, 50)
	betweenBlobs=0
	path='/Users/Sam/Desktop/regenProj/edgedBlobs/Make_1'
	name='edgeToEdge'
	filterOn=True
	flatBG=False
	touchingEdge=False
	addColors=False
	hasEdges=2

	testImage=Blob(numBlob, minSize, maxSize, blobThresh, innerThresh,
			sigma, shaderSigma, path, betweenBlobs, touchingEdge, flatBG, filterOn, addColors, name+'_'+str(i), hasEdges)
	testImage.makeImg()


