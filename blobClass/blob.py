from PIL import Image, ImageFilter
import matplotlib.cm as cm
import numpy as np
import random
import math
import copy

IMGSIZE = 100

# Used for debugging
def mirrorDiag(plot):
	new=np.zeros((IMGSIZE, IMGSIZE), dtype=np.int)
	for i in range(IMGSIZE):
		for j in range(IMGSIZE):
			new[i,j]=plot[j,i]
			new[j,i]=plot[i,j]
	return new

class Blob():

	def __init__(self, numBlob, minSize, maxSize, blobThresh, innerThresh, sigma, shaderSigma, dirPath, betweenBlobs, touchingEdge, flatBG, filterOn, addColors, name, hasEdges):
		# 0 if background pixel, else pixel represents which blob (1 for blob 1, 2 for blob 2 etc).
		self.imgType=np.zeros((IMGSIZE, IMGSIZE), dtype=np.int)
		# Holds val 0-255 for color intensity, 0=blue 255=red.
		self.imgPlot=np.zeros((IMGSIZE, IMGSIZE), dtype=np.int)
		# Number of blobs in image.
		self.numBlob=numBlob
		# Minimum and maximum permitted blob sizes.
		self.minSize=minSize
		self.maxSize=maxSize
		# Minimum color difference between neighboring blob and background pixels, 0-255.
		self.blobThresh=blobThresh
		# Maximum difference between neighboring pixels within a blob or background.
		self.innerThresh=innerThresh
		# Used to store pixel locations.
		self.typeList=[]
		self.blobList=[]
		self.outerList=[]
		# Current pixel selected, as (x, y) tuple.
		self.pix=None
		# 0 = filling binType, 1 = filling blob, 2 = filling background
		self.stage=0
		# current blob being filled
		self.blobNum=0
		# Unscaled sigma values for pixel and color selection.
		self.sigma=sigma
		self.shaderSigma=shaderSigma
		# Path of image file.
		self.dirPath=dirPath
		# Name of image file.
		self.name=name
		# Stores pixel locations.
		self.startPT=[]
		# Minimum allowable pixel distance between 2 blobs.
		self.betweenBlobs=betweenBlobs
		# True/False, True means blobs are not allowed to touch image borders.
		self.touchingEdge=touchingEdge
		# True/False, ets all background pixels to pure blue for class A images.
		self.flatBG=flatBG
		# True/False, True applies a smoothing filter to images.
		self.filterOn=filterOn
		# True/False, True changes color scheme of image for certain class D images.
		self.addColors=addColors
		# Blobs have edges (selects a random number of blobs to add edges to)
		self.hasEdges=hasEdges

	# Returns True if pixel at (x, y) is at least rad pixels from
	# any other blobs, else returns False.
	def clearSurrounding(self, x, y, rad):
		pixVal=[0, self.blobNum]
		for i in range(1+2*rad):
			a=i-rad
			for j in range(1+2*rad):
				b=j-rad
				if((0<=a+x<IMGSIZE) and (0<=b+y<IMGSIZE)):
					if(self.imgType[a+x][b+y] not in pixVal):
						return False
		return True

	# Finds a legal new pixel to add to shape, or add color to depending on stage of algorithm
	# and sets self.pix to new pixel location. Returns false if there are no avalible pixels,
	# else returns true.
	def getPix(self,size):
		# If choosing first pixel in shape.

		# if(self.hasEdges==2):
		# 	sqrt(size/np.pi)


		if(self.pix==None):
			if(self.touchingEdge==False):
				found=False
				while(found==False):
					print "found = false!"
					a=random.randint(0, (IMGSIZE-1))
					b=random.randint(0, (IMGSIZE-1))
					if(self.clearSurrounding(a, b, int(np.sqrt(size/np.pi)+4))==True):
						self.pix=(a, b)
						found=True
						self.startPT.append(self.pix)
				return True
			else:
				a=random.randint(29,69)
				b=random.randint(29,69)
				self.pix=(a,b)
				self.startPT.append(self.pix)
				return True
		# If finding pixels to add to shape.
		if(self.stage==0):
			localSigma=len(self.typeList)*(self.sigma/50)
			x=int(random.gauss(len(self.typeList), localSigma))
			if(x>len(self.typeList)):
				x=len(self.typeList)-(x-len(self.typeList))
			x=x-1
			if(x<0):
				x=0
			if(len(self.typeList)==0):
				return False
			self.pix=self.typeList[x]
			self.typeList.remove(self.pix)
			return True
		# If choosing pixels in shape/background to color.
		if(self.stage==1):
			if(len(self.blobList)==0):
				return False
			localSigma=len(self.blobList)*(self.sigma/50)
			x=int(random.gauss(len(self.blobList)/2, localSigma))
			if(x>len(self.blobList)):
				x=len(self.blobList)-(x-len(self.blobList))
			x=x-1
			self.pix=self.blobList.pop()
			return True

	# Returns True if pixel location is not within 3 pixels of image border,
	# else returns False.
	def isEdge(self, pix):
		coords=[0,1,2,IMGSIZE-3,IMGSIZE-2,IMGSIZE-1]
		if(((pix[0] in coords) or (pix[1] in coords)) and self.touchingEdge==True):
			return False
		else:
			return True

	# Adds legal neighbors to list of neighboring pixels
	def addNeighbors(self):
		neighborList=[]
		pix=self.pix
		if(self.stage==0):
			currentList=self.typeList
			pixType=0
		if(self.stage==1):
			currentList=self.blobList
			pixType=self.blobNum
		# Add neighbors above, below, left, and right.
		if(self.isEdge((pix[0]+1, pix[1])) and (pix[0]<(IMGSIZE-1)) and ((pix[0]+1, pix[1]) not in currentList)
			and (self.imgType[pix[0]+1, pix[1]]==pixType) and self.imgPlot[pix[0]+1, pix[1]]==0):
				neighborList.append((pix[0]+1, pix[1]))
		if(self.isEdge((pix[0]-1, pix[1])) and (pix[0]>0) and ((pix[0]-1, pix[1]) not in currentList)
			and (self.imgType[pix[0]-1, pix[1]]==pixType) and self.imgPlot[pix[0]-1, pix[1]]==0):
				neighborList.append((pix[0]-1, pix[1]))
		if(self.isEdge((pix[0], pix[1]+1)) and (pix[1]<(IMGSIZE-1)) and ((pix[0], pix[1]+1) not in currentList)
			and (self.imgType[pix[0], pix[1]+1]==pixType) and self.imgPlot[pix[0], pix[1]+1]==0):
				neighborList.append((pix[0], pix[1]+1))
		if(self.isEdge((pix[0], pix[1]-1)) and (pix[1]>0) and ((pix[0], pix[1]-1) not in currentList)
			and (self.imgType[pix[0], pix[1]-1]==pixType) and self.imgPlot[pix[0], pix[1]-1]==0):
				neighborList.append((pix[0], pix[1]-1))
		# Add neighbors on 4 diagonals with probability 0.5.
		if((self.stage==0 and random.randint(0, 1)==1) or (self.blobNum==0)):
			if(self.isEdge((pix[0]+1, pix[1]+1)) and (pix[0]<(IMGSIZE-1)) and (pix[1]<(IMGSIZE-1)) and self.imgPlot[pix[0]+1, pix[1]+1]==0
				and ((pix[0]+1, pix[1]+1) not in currentList) and (self.imgType[pix[0]+1, pix[1]+1]==pixType)):
				neighborList.append((pix[0]+1, pix[1]+1))
			if(self.isEdge((pix[0]+1, pix[1]-1)) and (pix[0]<(IMGSIZE-1)) and (pix[1]>0) and self.imgPlot[pix[0]+1, pix[1]-1]==0
				and ((pix[0]+1, pix[1]-1) not in currentList) and (self.imgType[pix[0]+1, pix[1]-1]==pixType)):
				neighborList.append((pix[0]+1, pix[1]-1))
			if(self.isEdge((pix[0]-1, pix[1]+1)) and (pix[0]>0) and (pix[1]<(IMGSIZE-1)) and self.imgPlot[pix[0]-1, pix[1]+1]==0
				and ((pix[0]-1, pix[1]+1) not in currentList) and (self.imgType[pix[0]-1, pix[1]+1]==pixType)):
				neighborList.append((pix[0]-1, pix[1]+1))
			if(self.isEdge((pix[0]-1, pix[1]-1)) and (pix[0]>0) and (pix[1]>0) and self.imgPlot[pix[0]-1, pix[1]-1]==0
				and ((pix[0]-1, pix[1]-1) not in currentList) and (self.imgType[pix[0]-1, pix[1]-1]==pixType)):
				neighborList.append((pix[0]-1, pix[1]-1))
		random.shuffle(neighborList)
		if(self.stage==0):
			self.typeList.extend(neighborList)
		if(self.stage==1):
			self.blobList.extend(neighborList)
	
	# Returns a list of all pixels in the background accessable by a BFS starting from image's
	# edge pixels. Note that if a "hole" contains a pixel along the border of the image it is
	# not considered a hole.					
	def holeBFS(self):
		vertices=[]
		for i in range(2):
			x=i*(IMGSIZE-1)
			for j in range(IMGSIZE):
				if(self.imgType[x, j]!=self.blobNum):
					vertices.append((x, j))
		for i in range(2):
			if(i==1):
				x=i*(IMGSIZE-1)
			else:
				x=0
			for j in range(IMGSIZE-2):
				if(self.imgType[j+1, x]!=self.blobNum):
					vertices.append((j+1, x))
		visited=[[0] * IMGSIZE for i in range(IMGSIZE)]
		count=0
		while(len(vertices)!=0):
			i=vertices.pop(0)
			if(visited[i[0]][i[1]]!=1):
				visited[i[0]][i[1]]=1
				if((i[0]-1)>0 and self.imgType[i[0]-1,i[1]]!=self.blobNum):
					if (i[0]-1,i[1]) not in vertices:
						vertices.append((i[0]-1, i[1]))
				if((i[0]+1)<(IMGSIZE-1) and self.imgType[i[0]+1,i[1]]!=self.blobNum):
					if (i[0]+1,i[1]) not in vertices:
						vertices.append((i[0]+1, i[1]))
				if((i[1]-1)>0 and self.imgType[i[0],i[1]-1]!=self.blobNum):
					if (i[0],i[1]-1) not in vertices:
						vertices.append((i[0], i[1]-1))
				if((i[1]+1)<(IMGSIZE-1) and self.imgType[i[0],i[1]+1]!=self.blobNum):
					if (i[0],i[1]+1) not in vertices:
						vertices.append((i[0], i[1]+1))
		return visited

	# Returns a list of pixels in holes using the list of background pixels
	# obtained from the holeBFS() method.
	def fillHoleBFS(self, visited):
		toFill=[]
		for i in range(IMGSIZE):
			for j in range(IMGSIZE):
				if(visited[i][j]!=1 and self.imgType[i,j]==0):
					toFill.append((i,j))
		return toFill

	# Returns a list of pixels in a given blob or background, sorted by distance from
	# "center of mass" of blob/background. This "center of mass" is the pixel with ~equal
	# numbers of pixels below, above, left, and right.
	def getList(self, blobNum):
		print 'Making list for blobNum '+str(blobNum)
		center=[0.0,0.0]
		wWeight=[0]*IMGSIZE
		hWeight=[0]*IMGSIZE
		blobList=[]
		for i in range(IMGSIZE):
			for j in range(IMGSIZE):
				if(self.imgType[i][j]==blobNum):
					blobList.append((i,j))
					wWeight[i]=wWeight[i]+1
					hWeight[j]=hWeight[j]+1
		print 'blobList has length '+str(len(blobList))
		if len(blobList)==1:
			for i in range(IMGSIZE):
				for j in range(IMGSIZE):
					if(self.imgType[i][j]==blobNum):
						print 'pix in blob!'

		wPoint=0
		hPoint=0
		wBal=np.zeros((IMGSIZE), dtype=np.int)
		hBal=np.zeros((IMGSIZE), dtype=np.int)
		for i in range(IMGSIZE):
			# Width balancing
			lWeight=0
			rWeight=0
			l=i-1
			r=i+1
			while(l>=0):
				lWeight=lWeight+wWeight[l]
				l=l-1
			while(r<IMGSIZE):
				rWeight=rWeight+wWeight[r]
				r=r+1
			wBal[i]=abs(rWeight+lWeight)
			# Height balancing
			tWeight=0
			bWeight=0
			t=i-1
			b=i+1
			while(t>=0):
				tWeight=tWeight+hWeight[t]
				t=t-1
			while(b<IMGSIZE):
				bWeight=bWeight+hWeight[b]
				b=b+1
			hBal[i]=abs(tWeight+bWeight)
		wIndex=wBal.argmin()
		hIndex=hBal.argmin()
		blobList.sort(key=lambda x: abs(0-abs(x[0]-wIndex)-abs(x[1]-hIndex)))
		return blobList

	# Returns a tuple of min and max allowable color intenseties for a given
	# pixel, as well as the average color intensity of neighboring pixels in the
	# same blob/background.
	def getLegalShades(self):
		if(self.imgType[self.pix[0], self.pix[1]]==0):
			if(self.flatBG==True):
				shades=[1,1]
			else:
				shades=[1, 255-self.blobThresh]
		else:
			shades=[self.blobThresh+1, 255]
		seq=[-1, 0, 1]
		avgShade=[0, 0]
		for i in seq:
			a=self.pix[0]+i
			for j in seq:
				b=self.pix[1]+j
				# Don't check shade for selected pix, only for neighbors
				if(i==j==0):
					continue
				if((0<=a<IMGSIZE) and (0<=b<IMGSIZE)):
					if(self.imgPlot[a, b]==0):
						continue
					# Make sure blob thresh can be met by any border cells.
					if (self.imgType[a,b]==0 and shades[1]>255-self.blobThresh):
						shades[1]=255-self.blobThresh
					if (self.imgType[a,b]>0 and shades[0]<1+self.blobThresh):
						shades[0]=self.blobThresh+1
					if(self.imgType[a,b]!=self.imgType[self.pix[0], self.pix[1]] and self.imgPlot[a, b]!=0):
						if(self.imgType[a,b]==0):#In a blob next to non-blob
							if(shades[0]>(self.imgPlot[a,b]+self.blobThresh)):
								shades[0]=self.imgPlot[a,b]+self.blobThresh
						if(self.imgType[a,b]!=0):#In non-blob next to blob
							if(shades[1]>(self.imgPlot[a,b]-self.blobThresh)):
								shades[1]=self.imgPlot[a,b]-self.blobThresh
					if(self.imgType[a,b]==self.imgType[self.pix[0], self.pix[1]] and self.imgPlot[a, b]!=0):
						avgShade[0]=avgShade[0]+1
						avgShade[1]=avgShade[1]+self.imgPlot[a, b]
						if(shades[0]<(self.imgPlot[a,b]-self.innerThresh)):
							shades[0]=self.imgPlot[a,b]-self.innerThresh
						if(shades[1]>(self.imgPlot[a,b]+self.innerThresh)):
							shades[1]=self.imgPlot[a,b]+self.innerThresh
		if(shades[0]>shades[1]):
					x=(shades[0]+shades[1])/2
					shades[0]=x
					shades[1]=x
		if(avgShade[0]!=0):
			# If neighboring pix are shaded already, let their colors influence
			avgShade=avgShade[1]/avgShade[0]
		else:
			# Otherwise pick random allowable color instead of local average
			avgShade=random.randint(shades[0], shades[1])
		# print avgShade
		return (shades[0], shades[1]), avgShade
	
	# Picks a color value for each pixel and records it.	
	def fillShades(self):
		if(self.hasEdges==2):
			maxBlobs=self.numBlob+2
		else:
			maxBlobs=self.numBlob+1

# BACKGROUND CONTROL!!!! 0/1

		for i in range(0,maxBlobs):
			print "Blob "+str(i)
			pixList=self.getList(i)
			for j in pixList:
				self.pix=j
				shades, avgShade=self.getLegalShades()
				avgShade=np.clip([avgShade], shades[0], shades[1])
				avgShade=avgShade[0]
				sig=int((float(self.shaderSigma)/100)*(shades[1]-shades[0]))
				x=int(random.gauss(avgShade, sig))
				if(x>shades[1]):
					x=shades[1]-(x-shades[1])
				if(x<shades[0]):
					x=shades[0]
				self.imgPlot[self.pix[0], self.pix[1]]=x

	# Get slope instead of choosing 2 pts because square would make diagonal lines more probably than vert/horiz. lines
	def addEdges(self):
		# intersectPlot=copy.deepcopy(self.imgType)
		print "finding intersect"
		fromCenter = self.getList(self.blobNum)
		print 'fromCenter has len '+str(len(fromCenter))
		intersect = fromCenter[random.randrange(0,len(fromCenter)/4)]
		up=IMGSIZE-intersect[1]
		right=IMGSIZE-intersect[0]
		down=intersect[1]
		left=intersect[0]
		if up>down:
			rise=random.randrange(0, up)
		else:
			rise=random.randrange(-down, 1)
		if right>left:
			run=random.randrange(0, right)
		else:
			run=random.randrange(-left, 1)
		if run==0:
			slope=1
		else:
			slope=float(rise)/float(run)
		a=intersect
		b=(intersect[0]+run, intersect[1]+rise)
		# for i in toAddEdge:
		blobSideA=[]
		blobSideB=[]
		for x in range(IMGSIZE):
			for y in range(IMGSIZE):
				# print self.imgType[x, y]
				c=(x,y)
				if self.imgType[x, y]==self.blobNum:
					if self.isAboveLine(a, b, (x, y)):
						blobSideA.append((x,y))
					else:
						blobSideB.append((x,y))
		if random.getrandbits(1):
			self.deleteCells(blobSideA, blobSideB, 'A')
		else:
			self.deleteCells(blobSideA, blobSideB, 'B')

	def colorHalf(self):
		# self.hasEdges
		# if self.hasEdges==2:
		print 'In color half!'
		readyFill=False
		# for i in range(IMGSIZE):
		# 	for j in range(IMGSIZE):
		# 		self.imgType[i, j]=0
		while readyFill==False:
			# print "finding intersect"
			# fromCenter = self.getList(self.blobNum)
			# print 'fromCenter has len '+str(len(fromCenter))
			# intersect = fromCenter[random.randrange(0,len(fromCenter)/4)]
			if self.hasEdges==2:
				intersect=(random.randrange(int(IMGSIZE*0.05), int(IMGSIZE*0.95)), random.randrange(int(IMGSIZE*0.05), int(IMGSIZE*0.95)))
			elif self.hasEdges==3:
				print "it's 3!"
				found=False
				intBlob = 0
				while found==False:
					i=random.randint(0, IMGSIZE-1)
					j=random.randint(0, IMGSIZE-1)
					if self.imgType[i, j] != 0:
						intBlob = self.imgType[i, j]
						intersect = (i, j)
						found = True
						print self.imgType[i, j]
				print "color half found = "+str(found)

			up=IMGSIZE-intersect[1]
			right=IMGSIZE-intersect[0]
			down=intersect[1]
			left=intersect[0]
			if up>down:
				rise=random.randrange(0, up)
			else:
				rise=random.randrange(-down, 1)
			if right>left:
				run=random.randrange(0, right)
			else:
				run=random.randrange(-left, 1)
			if run==0:
				slope=1
			else:
				slope=float(rise)/float(run)
			a=intersect
			b=(intersect[0]+run, intersect[1]+rise)
			toColor=[]
			for i in range(IMGSIZE):
				for j in range(IMGSIZE):
					if self.isAboveLine(a, b, (i, j)):
						# print "Coloring!!"
						toColor.append((i, j))
			print 'toColor has '+str(len(toColor))+ 'cells'
			if len(toColor)>0.8*IMGSIZE*IMGSIZE:
				# print "continuing!"
				continue
			else:
				for cell in toColor:
					if self.hasEdges==2:
						# print "cell is "+str((cell[0], cell[1]))
						self.imgType[cell[0], cell[1]]=self.numBlob+1
						# print self.imgType[cell[0], cell[1]]
					elif self.hasEdges==3:
						# print "changing!!!!!!"
						if self.imgType[cell[0], cell[1]]==0:
							self.imgType[cell[0], cell[1]]=intBlob
						elif self.imgType[cell[0], cell[1]]==intBlob:
							continue
						else:
							self.imgType[cell[0], cell[1]]=0
				readyFill=True




		# for cx in intersectPlot[0]:
		# 	for cy in intersectPlot[1]:
		# 		if isAboveLine(a, b, (cx, cy)):
		# 			intersectPlot[cx, cy]=1
	"""
		Copy img type plot
		Use blob self.numBlob
		copy cells from current blob to intersect plot
		Make a line
		Make 2 lists, lSideA, lSideB, one holding cells on each side of line
		Randomly pick one list, suppose A is picked

		if len(A)>(len(a)+len(b))/10
			erase cells in list A
		else
			erase cells in list B		
	"""



		# x=intersect[0]
		# y=intersect[1]
		# while x<IMGSIZE and y<IMGSIZE:
		# 	intersectPlot[x][y]=1
		# for x in range(IMGSIZE):
		# 	y=

	def isAboveLine(self, a, b, c):
		return ((b[0] - a[0])*(c[1] - a[1]) - (b[1] - a[1])*(c[0] - a[0])) > 0

	def deleteCells(self, blobSideA, blobSideB, side):
		if side=='A':
			toDelete=blobSideA
		else:
			toDelete=blobSideB
		for x in range(IMGSIZE):
			for y in range(IMGSIZE):
				if (x,y) in toDelete:
					self.imgType[x, y]=0
		# elif len(blobSideB)>(len(blobSideA)+len(blobSideB))/5:
		# 	toDelete=blobSideB
		# 	for x in range(IMGSIZE):
		# 		for y in range(IMGSIZE):
		# 			if (x,y) in toDelete:
		# 				self.imgType[x, y]=0
	
	# Main method.
	def makeImg(self):
		img=Image.new('RGB', (IMGSIZE,IMGSIZE), 'white')
		print '\nMaking image: '+self.name

		# Choose which pixels belong to which blobs.
		print 'This image has '+str(self.numBlob)+' blobs'
		if(self.hasEdges==2):
			self.colorHalf()
			pixInBlob=0
			for x in range(IMGSIZE):
				for y in range(IMGSIZE):
					if self.imgType[x,y]==self.numBlob+1:
						pixInBlob += 1
			print 'pixInBlob = '+str(pixInBlob)
		for i in range(self.numBlob):
			self.blobNum=i+1
			print '\nGenerating blobNum '+str(self.blobNum)
			blobSize = random.randint(self.minSize, self.maxSize)
			print 'This blob has ' +str(blobSize)+' pixels'
			for j in range(blobSize):
				if(self.getPix(blobSize)==False):
					break
				# Find first pixel for blob i.
				if(j==0):
					if(self.clearSurrounding(self.pix[0], self.pix[1], IMGSIZE*(1/3))==False):
						goodPix=False
						while(goodPix==False):
							if(self.getPix(blobSize)==False):
								break
							if(self.clearSurrounding(self.pix[0], self.pix[1], IMGSIZE*(1/3))==True):
								goodPix=True
				else:
					if(self.clearSurrounding(self.pix[0], self.pix[1], self.betweenBlobs)==False):
						goodPix=False
						while(goodPix==False):
							if(self.getPix(blobSize)==False):
								break
							if(self.clearSurrounding(self.pix[0], self.pix[1], self.betweenBlobs)==True):
								goodPix=True
				self.addNeighbors()
				self.imgType[self.pix[0], self.pix[1]] = self.blobNum

				# Search for holes
				if((j==(blobSize/2)) or (j==(3*blobSize/4)) or j==blobSize-1):
					visited=self.holeBFS()
					toFill=self.fillHoleBFS(visited)
					j=j-len(toFill)
					for k in toFill:
						self.imgType[k[0],k[1]]=self.blobNum
			# Add edges to blob(s)
			if self.hasEdges==1:
				if self.blobNum==1:
					self.addEdges()
				elif random.getrandbits(1):
					self.addEdges()
			# elif(self.hasEdges==2 and self.blobNum==self.numBlob):
			# 	self.colorHalf()
			# 	pixInBlob=0
			# 	for x in range(IMGSIZE):
			# 		for y in range(IMGSIZE):
			# 			if self.imgType[x,y]==self.blobNum:
			# 				pixInBlob += 1
			# 	print 'pixInBlob = '+str(pixInBlob)
			self.pix=None
			self.typeList=[]
		if self.hasEdges==3:
			print "------------HAS EDGES = 3!!!"
			self.colorHalf()
		# Begin choosing colors for each pixel.
		self.stage=1
		self.fillShades()
		if(self.blobNum==1):
			self.blobNum=self.numBlob+1
			self.fillShades()
		toSave=img.load()

		# Change color scheme for certain class D images.
		if(self.addColors==True):
			# 0 - 1 and 2
			# 1 - randomly swap colors representing blobs/background
			# 2 - add third color (variable)
			colorMod=random.randint(0,2)
			if(colorMod==0):
				vals=[0,1,2]
				a=random.choice(vals)
				vals.remove(a)
				b=random.choice(vals)
				vals.remove(b)
				c=vals[0]
				for i in range(IMGSIZE):
					for j in range(IMGSIZE):
						toMix=[self.imgPlot[i,j],0,255-self.imgPlot[i,j]]
						toSave[i,j]=(toMix[a],toMix[b],toMix[c])
			elif(colorMod==1):
				if(bool(random.getrandbits(1))==True):
					green=random.randint(0,255)
					for i in range(IMGSIZE):
						for j in range(IMGSIZE):
							toSave[i,j]=(self.imgPlot[i,j],green,255-self.imgPlot[i,j])
				else:
					for i in range(IMGSIZE):
						for j in range(IMGSIZE):
							toSave[i,j]=(self.imgPlot[i,j],random.randint(0,255),255-self.imgPlot[i,j])
			elif(colorMod==2):
				if(bool(random.getrandbits(1))):
					vals=[0,1,2]()
					a=random.choice(vals)
					vals.remove(a)
					b=random.choice(vals)
					vals.remove(b)
					c=vals[0]
					for i in range(IMGSIZE):
						for j in range(IMGSIZE):
							toMix=[self.imgPlot[i,j],random.randint(0,255),255-self.imgPlot[i,j]]
							toSave[i,j]=(toMix[a],toMix[b],toMix[c])
				else:
					vals=[0,1,2]
					a=random.choice(vals)
					vals.remove(a)
					b=random.choice(vals)
					vals.remove(b)
					c=vals[0]
					green=random.randint(0,255)
					for i in range(IMGSIZE):
						for j in range(IMGSIZE):
							toMix=[self.imgPlot[i,j],green,255-self.imgPlot[i,j]]
							toSave[i,j]=(toMix[a],toMix[b],toMix[c])

		else:



			# for i in range(IMGSIZE):
			# 	for j in range(IMGSIZE):
					# toSave[i,j]=(self.imgPlot[i,j],0,255-self.imgPlot[i,j])
					# if self.imgPlot[i,j] > 127:
					# 	toSave[i,j] = (2*(127-self.imgPlot[i,j]), 0, 0)
					# 	print "Greater! "+str(toSave[i,j])+" "+str(self.imgPlot[i,j])+" "+str(2*(127-self.imgPlot[i,j]))
					# elif self.imgPlot[i,j] < 127:
					# 	toSave[i,j] = (0, 0, 2*(self.imgPlot[i,j]-127))
					# 	print "Less! "+str(toSave[i,j])+" "+str(self.imgPlot[i,j])+" "+str(2*(self.imgPlot[i,j]-127))
					# else:
					# 	toSave[i,j] = (255, 255, 255)
					# 	print "Neutral! "+str(toSave[i,j])

			for i in range(IMGSIZE):
				for j in range(IMGSIZE):
					norm_tup = cm.coolwarm(self.imgPlot[i,j])#m.to_rgba(i)#/255.0)
					reg = (int(norm_tup[0]*255), int(norm_tup[1]*255), int(norm_tup[2]*255))
					# print reg
					toSave[i, j] = reg


		# Apply smoothing filter if class A img.
		if(self.filterOn==True):
			img=img.filter(ImageFilter.BLUR)
		img.save(self.dirPath + '/' + self.name + '.png')

