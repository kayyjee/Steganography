import os, sys, binascii
from Crypto.Cipher import AES
from Crypto import Random
import hashlib
from PIL import Image


binDataString =""
binDataSize =""






def createString(secretData):
	
	global binDataString
	global binDataSize
	

	binName = ""
	nullDelimiter = "00000000"

	

	for bits in secretData:
		binName += format(ord(bits), 'b').zfill(8)#convert the file name to binary
	

	fileData = bytearray(open(secretData, 'rb').read())#opens the binary file in read or write mode 
	for bits in fileData:
		binDataString += bin(bits)[2:].zfill(8)#convert the file data to binary

	dataSize = list(str(len(binDataString)))#data size as a list of each int

	for bits in dataSize:
		binDataSize += format(ord(bits), 'b').zfill(8)#convert the data size to binary
	
	

	bitString = binName+nullDelimiter+binDataSize+nullDelimiter+binDataString#assemble string with NULL delimiters
	


	#if len(headerString)%16 != 0:
#		headerString +=nullDelimiter
	return bitString


def getDecimalPixelRGB(rgb):
	rgba_decimal_array = []
	
	for colour_value in rgb:
		rgba_decimal_array.append(int(''.join(str(b) for b in colour_value), 2))

	return (rgba_decimal_array[0], rgba_decimal_array[1], rgba_decimal_array[2])






def encode(coverImage, secretData, outputFileName, password):
	bitString = createString(secretData)#string contains the header, data and length in binary
	imageObj = Image.open(coverImage).convert('RGB')
	imgWidth, imgHeight = imageObj.size
	pixels = imageObj.load()
	rgbArray = []
	count=0

	for x in range (imgWidth):
		for y in range (imgHeight):
			r,g,b = pixels[x,y]

			

			redPixel = list(bin(r)[2:].zfill(8))
			greenPixel = list(bin(g)[2:].zfill(8))
			bluePixel = list(bin(b)[2:].zfill(8))

			pixelList = [redPixel, greenPixel, bluePixel]
			



			for i in range(0,3):

				if count >= len(bitString):
					
					for rgbValue in pixelList:
						rgbArray.append(int(''.join(str(b) for b in rgbValue), 2))

					pixels[x, y] = (rgbArray[0], rgbArray[1], rgbArray[2])
					
					print "Completed"
					return imageObj.save(outputFileName)





				else:
					pixelList[i][7] = bitString[count]
					count+=1


	#pixels[x,y] = getDecimalPixelRGB(pixelList)
	#print "Completed"


def toString(string):
	return binascii.unhexlify('%x' % int(string[:-8], 2))


def saveImage(lsbByteString, outputFileName, fileSize):
	secretData=[]
	print int(fileSize)/8
	for i in range(int(fileSize) /8):
		secretData.append(int(lsbByteString[i*8:(i+1) * 8], 2))
		

	secretFileBytes = bytearray(secretData)

	fileHandler = open(outputFileName, 'w')
	fileHandler.write(secretFileBytes)
	return()


def decode(imagePath, outputFileName, password):
	imageObj = Image.open(imagePath).convert('RGB')
	imgWidth, imgHeight = imageObj.size
	pixels = imageObj.load()
	lsbString=""#storing all the lsb's
	lsbByteString=""#storing lsb's in groups of 8
	secretFileString=""
	count = 0
	fileNameReceived = 0
	fileSizeReceived = 0

	for x in range(imgWidth):
		for y in range(imgHeight):
			r,g,b = pixels[x,y]
			
			redPixel = list(bin(r)[2:].zfill(8))
			greenPixel = list(bin(g)[2:].zfill(8))
			bluePixel = list(bin(b)[2:].zfill(8))
			
			pixelList = [redPixel, greenPixel, bluePixel]


			for i in range(0,3):
				lsbString += pixelList[i][7]


				if len(lsbString)==8:#we have a byte, check


					lsbByteString += lsbString

					if lsbString == "00000000":#null character is delimiter
						if fileNameReceived != 1:
							fileName = toString(lsbByteString)
							print "File name: " + fileName
							fileNameReceived = 1
						

						elif fileSizeReceived !=1:
							fileSize = toString(lsbByteString)
							print "File size: " + fileSize
							fileSizeReceived = 1 



						lsbByteString =""
					lsbString =""


							
				if  (fileSizeReceived == 1  and fileNameReceived == 1):
					
					if  int(fileSize) > int(count):
						secretFileString += pixelList[i][7]
						count += 1
					
					else:
						
						saveImage(secretFileString, outputFileName, fileSize)
						return
					


						










					


				#pixelList

