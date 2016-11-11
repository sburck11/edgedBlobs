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
# for i in range(20):
# 	numBlob=random.randrange(1,2)
# 	minSize=250
# 	maxSize=1000
# 	blobThresh=random.randint(180, 220)
# 	innerThresh=random.randint(10, 20)
# 	sigma=120#random.randint(90, 120)
# 	shaderSigma=random.randint(15, 20)
# 	betweenBlobs=0
# 	path='/Users/Sam/Desktop/regenProj/edgedBlobs/Make_1'
# 	name='edgeToEdge'
# 	filterOn=True
# 	flatBG=False
# 	touchingEdge=False
# 	addColors=False
# 	hasEdges=2

	# testImage=Blob(numBlob, minSize, maxSize, blobThresh, innerThresh,
	# 		sigma, shaderSigma, path, betweenBlobs, touchingEdge, flatBG, filterOn, addColors, name*"_"+str(i), hasEdges)
	# testImage.makeImg()
for i in range(4):
	numBlob=random.randrange(1,4)
	minSize=200
	maxSize=500
	blobThresh=random.randint(100, 220)
	innerThresh=random.randint(5, 65)
	sigma=random.randint(40, 100)
	shaderSigma=random.randint(25, 120)
	betweenBlobs=0
	path='/Users/Sam/Desktop/regenProj/edgedBlobs/Make_1'
	name='edgeToEdge'
	filterOn=True
	flatBG=False
	touchingEdge=False
	addColors=False
	hasEdges=0



	testImage=Blob(numBlob, minSize, maxSize, blobThresh, innerThresh,
			sigma, shaderSigma, path, betweenBlobs, touchingEdge, flatBG, filterOn, addColors, name+'_'+str(i), hasEdges)
	testImage.makeImg()


