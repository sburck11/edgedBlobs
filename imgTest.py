from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import random
from blobClass.blob import Blob
from pathos.multiprocessing import ProcessingPool

numImages = 16
numBlob=2
minSize=800
maxSize=1800
blobThresh=100
innerThresh=50
sigma=55
shaderSigma=30
betweenBlobs=5
path='/Users/Sam/Desktop/regenProj/Blob_Images/blobClass1'
# 'mp' for multiprocessing, 'mt' for multithreading
MODE='mp'




# A: There are no blobs touching the line. Colors are very homogeneous
# (little/no pixelation), and the line is a solid edge (so very little blur).

# B: There are either blobs touching the line, or there is pixelation and blur.

# C: There are blobs touching the line, and there's pixelation and blur or
#  	class E, so just edged blobs, not edge across whole image

# D: Some clean blobs without any line/edge, and some messy/noisy images without any line/edge.

# ~1 sec/img for nodes=4 on 4-core cpu
pool=ProcessingPool(nodes=4)	
imgArr=[]
for i in range(numImages):
	# Type 1 = Class A, Type 4 = Class D.
	type=random.randint(1,4)
	addColors=False
	if(type==4):
		# GRADE D, WORST CASE!
		filterOn=False
		flatBG=False
		numBlob=random.randint(0, 3)
		if(numBlob==1):
			numBlob=random.randint(2,3)
		touchingEdge=False
		sigma=random.randint(5, 40)
		shaderSigma=random.randint(1, 30)
		minSize=random.randint(800, 1000)
		maxSize=random.randint(1000, 3000)
		blobThresh=random.randint(30, 120)
		innerThresh=random.randint(40, 180)
		name='D_'+str(i)
		if(bool(random.getrandbits(1))):
			addColors=True
	elif(type==3):
		# Grade C
		filterOn=False
		flatBG=False
		touchingEdge=False
		flaw=random.randint(0,2)
		if(flaw==0):
			# 1 Blob
			numBlob=1
			touchingEdge=True
			sigma=50
			shaderSigma=random.randint(40, 100)
			blobThresh=random.randint(100, 120)
			innerThresh=random.randint(120, 180)
			minSize=random.randint(400, 600)
			maxSize=random.randint(800, 1200)
		elif(flaw==1):
			# Not Jagged
			numBlob=random.randint(2,3)
			sigma=random.randint(130, 180)
			shaderSigma=random.randint(25, 50)
			blobThresh=random.randint(100, 120)
			innerThresh=random.randint(70, 90)
			minSize=random.randint(500, 800)
			maxSize=random.randint(1000, 1500)
		else:
			# Not pixelated
			flatBG=True
			numBlob=random.randint(2,3)
			minSize=random.randint(500, 800)
			maxSize=random.randint(1000, 1250)
			sigma=50
			shaderSigma=random.randint(100, 150)
			blobThresh=random.randint(120, 150)
			innerThresh=random.randint(5, 15)
		name='C_'+str(i)
	elif(type==2):
		# Grade B
		filterOn=False
		numBlob=1
		touchingEdge=False
		flaw=random.randint(0,2)
		if(flaw==0):
			# 1 Blob, Not Jagged
			numBlob=1
			touchingEdge=True
			flatBG=False
			filterOn=True
			sigma=random.randint(130, 250)
			shaderSigma=random.randint(25, 50)
			blobThresh=random.randint(100, 120)
			innerThresh=random.randint(40, 60)
			minSize=random.randint(400, 600)
			maxSize=random.randint(800, 1200)
		elif(flaw==1):
			# 1 Blob, Not Pixelated
			numBlob=1
			flatBG=True
			touchingEdge=True
			filterOn=False
			sigma=50
			shaderSigma=random.randint(5, 20)
			blobThresh=random.randint(150, 180)
			innerThresh=random.randint(5, 10)
			minSize=random.randint(750, 1000)
			maxSize=random.randint(1500, 2000)
		else:
			# Mult blobs, Not Jagged, Not Pixelated
			numBlob=random.randint(2,3)
			filterOn=True
			flatBG=True
			touchingEdge=False
			sigma=random.randint(160, 225)
			shaderSigma=random.randint(15, 20)
			minSize=random.randint(500, 750)
			maxSize=1000
			blobThresh=random.randint(150, 180)
			innerThresh=random.randint(10, 25)
			# name='B2_'+str(i)
		name='B_'+str(i)
	else:
		# GRADE A
		filterOn=True
		flatBG=True
		numBlob=1
		touchingEdge=True
		sigma=120
		shaderSigma=random.randint(15, 20)
		minSize=random.randint(500, 750)
		maxSize=random.randint(1000, 2000)
		blobThresh=random.randint(180, 250)
		innerThresh=random.randint(10, 20)
		name='A_'+str(i)

	testImage=Blob(numBlob, minSize, maxSize, blobThresh, innerThresh,
		sigma, shaderSigma, path, betweenBlobs, touchingEdge, flatBG, filterOn, addColors, name)
	imgArr.append(testImage)

pool.map(Blob.makeImg, imgArr)

# A

# for i in range(20):
# 	numBlob=random.randrange(1,2)
# 	minSize=250
# 	maxSize=1000
# 	blobThresh=random.randint(180, 220)
# 	innerThresh=random.randint(10, 15)
# 	sigma=120#random.randint(90, 120)
# 	shaderSigma=random.randint(15, 60)
# 	betweenBlobs=0
# 	path='/Users/Sam/Desktop/regenProj/edgedBlobs/Make_1'
# 	name='edgeToEdge'
# 	filterOn=True
# 	flatBG=False
# 	touchingEdge=False
# 	addColors=False
# 	hasEdges=2

# E:

# for i in range(5):
# 	numBlob=random.randrange(1,2)
# 	minSize=1000
# 	maxSize=2000
# 	blobThresh=random.randint(180, 220)
# 	innerThresh=random.randint(10, 20)
# 	sigma=120#random.randint(90, 120)
# 	shaderSigma=random.randint(15, 20)
# 	betweenBlobs=0
# 	path='/Users/Sam/Desktop/regenProj/edgedBlobs/Make_1'
# 	name='edgeToEdge'
# 	filterOn=True
# 	flatBG=False
# 	touchingEdge=True
# 	addColors=False
# 	hasEdges=1






