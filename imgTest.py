from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import random
from blobClass.blob import Blob
from pathos.multiprocessing import ProcessingPool

numImages = 5000
# numBlob=2
# minSize=800
# maxSize=1800
# blobThresh=100
# innerThresh=50
# sigma=55
# shaderSigma=30
# betweenBlobs=5
path='/Users/Sam/Desktop/regenProj/edgedBlobs/Training_Set'
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
		numBlob=random.randrange(1,4)
		minSize=200
		maxSize=500
		blobThresh=random.randint(100, 220)
		innerThresh=random.randint(5, 65)
		sigma=random.randint(40, 100)
		shaderSigma=random.randint(25, 120)
		betweenBlobs=0
		filterOn=True
		flatBG=False
		touchingEdge=False
		addColors=False
		hasEdges=0
		name='D_'+str(i)
	elif(type==3):
		# Grade C, E
		filterOn=False
		flatBG=False
		touchingEdge=False
		flaw=random.randint(0,1)
		if(flaw==0):
			# Grade C
			numBlob=random.randrange(2,4)
			minSize=200
			maxSize=350
			blobThresh=random.randint(120, 160)
			innerThresh=random.randint(10, 50)
			sigma=random.randint(75, 120)
			shaderSigma=random.randint(35, 75)
			betweenBlobs=0
			filterOn=True
			flatBG=False
			touchingEdge=False
			addColors=False
			hasEdges=3
			name='C_'+str(i)
		elif(flaw==1):
			# Grade E
			numBlob=random.randrange(1,2)
			minSize=1000
			maxSize=2000
			blobThresh=random.randint(180, 220)
			innerThresh=random.randint(10, 20)
			sigma=120#random.randint(90, 120)
			shaderSigma=random.randint(15, 50)
			betweenBlobs=0
			filterOn=True
			flatBG=False
			touchingEdge=True
			addColors=False
			hasEdges=1
			name='E_'+str(i)
		
	elif(type==2):
		# Grade B
		flaw=random.randint(0,1)
		if(flaw==0):
			# Pixelated
			numBlob=random.randrange(1,2)
			minSize=250
			maxSize=400
			blobThresh=random.randint(120, 200)
			innerThresh=random.randint(20, 50)
			sigma=120#random.randint(90, 120)
			shaderSigma=random.randint(35, 75)
			betweenBlobs=0
			filterOn=True
			flatBG=False
			touchingEdge=False
			addColors=False
			hasEdges=2
		else:
			# Touching line
			numBlob=random.randrange(3,4)
			minSize=250
			maxSize=400
			blobThresh=random.randint(180, 220)
			innerThresh=random.randint(40, 50)
			sigma=120#random.randint(90, 120)
			shaderSigma=random.randint(5, 10)
			betweenBlobs=0
			filterOn=True
			flatBG=True
			touchingEdge=False
			addColors=False
			hasEdges=3
		name='B_'+str(i)
	else:
		# GRADE A
		numBlob=random.randrange(1,2)
		minSize=250
		maxSize=1000
		blobThresh=random.randint(180, 220)
		innerThresh=random.randint(10, 15)
		sigma=120#random.randint(90, 120)
		shaderSigma=random.randint(30, 60)
		betweenBlobs=0
		filterOn=True
		flatBG=True
		touchingEdge=False
		addColors=False
		hasEdges=2
		name='A_'+str(i)

	testImage=Blob(numBlob, minSize, maxSize, blobThresh, innerThresh,
		sigma, shaderSigma, path, betweenBlobs, touchingEdge, flatBG, filterOn, addColors, name, hasEdges)
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

# B:
	# Touching line

	# numBlob=random.randrange(3,4)
	# minSize=250
	# maxSize=400
	# blobThresh=random.randint(180, 220)
	# innerThresh=random.randint(40, 50)
	# sigma=120#random.randint(90, 120)
	# shaderSigma=random.randint(5, 10)
	# betweenBlobs=0
	# path='/Users/Sam/Desktop/regenProj/edgedBlobs/Make_1'
	# name='edgeToEdge'
	# filterOn=True
	# flatBG=True
	# touchingEdge=False
	# addColors=False
	# hasEdges=3

	# Pixelated

	# numBlob=random.randrange(1,2)
	# minSize=250
	# maxSize=400
	# blobThresh=random.randint(120, 200)
	# innerThresh=random.randint(20, 50)
	# sigma=120#random.randint(90, 120)
	# shaderSigma=random.randint(35, 75)
	# betweenBlobs=0
	# path='/Users/Sam/Desktop/regenProj/edgedBlobs/Make_1'
	# name='edgeToEdge'
	# filterOn=False
	# flatBG=False
	# touchingEdge=False
	# addColors=False
	# hasEdges=2

# C:

	# numBlob=random.randrange(2,4)
	# minSize=200
	# maxSize=350
	# blobThresh=random.randint(120, 160)
	# innerThresh=random.randint(10, 50)
	# sigma=random.randint(45, 90)
	# shaderSigma=random.randint(35, 75)
	# betweenBlobs=0
	# path='/Users/Sam/Desktop/regenProj/edgedBlobs/Make_1'
	# name='edgeToEdge'
	# filterOn=True
	# flatBG=False
	# touchingEdge=False
	# addColors=False
	# hasEdges=3

# D:

	# numBlob=random.randrange(1,4)
	# minSize=200
	# maxSize=500
	# blobThresh=random.randint(100, 220)
	# innerThresh=random.randint(5, 65)
	# sigma=random.randint(40, 100)
	# shaderSigma=random.randint(25, 120)
	# betweenBlobs=0
	# path='/Users/Sam/Desktop/regenProj/edgedBlobs/Make_1'
	# name='edgeToEdge'
	# filterOn=True
	# flatBG=False
	# touchingEdge=False
	# addColors=False
	# hasEdges=0

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






