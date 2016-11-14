import os, sys, binascii, array
from Crypto.Cipher import AES
from Crypto import Random
import hashlib
from PIL import Image
import dcimage

#examine the lsb of each pixel, grouping into bytes
#check for nulls to signify if we are dealing with data or header info
#bytes determined to be data result in the hidden file
def encode(imagePath, secretData, outputFileName, password):
	bitString = dcimage.createString(secretData)#string contains the header, data and length in binary
	imageObj = Image.open(imagePath).convert('RGB')
	imgWidth, imgHeight = imageObj.size
	pixels = imageObj.load()
	rgbDecimalArray = []
	rgbArray = []
	count=0#iterator

	#cycle through each pixel
	for x in range (imgWidth):
		for y in range (imgHeight):
			r,g,b = pixels[x,y]
			#convert each pixel into an 8 bit representation
			redPixel = list(bin(r)[2:].zfill(8))
			greenPixel = list(bin(g)[2:].zfill(8))
			bluePixel = list(bin(b)[2:].zfill(8))
			pixelList = [redPixel, greenPixel, bluePixel]

			#for each of rgb
			for i in range(0,3):
				#verify we have reached the end of our hidden file
				if count >= len(bitString):
					#convert the bits to their rgb value and appned them 
					for rgbValue in pixelList:
						rgbArray.append(int(''.join(str(b) for b in rgbValue), 2))
					pixels[x, y] = (rgbArray[0], rgbArray[1], rgbArray[2])
					print "Completed"
					return imageObj.save(outputFileName)

				#If we haven't rached the end of the file, store a bit
				else:
					pixelList[i][7] = bitString[count]
					count+=1
			pixels[x, y] = dcimage.getPixel(pixelList)
			


#examine the lsb of each pixel, grouping into bytes
#check for nulls to signify if we are dealing with data or header info
#bytes determined to be data result in the hidden file
def decode(imagePath, outputFileName, password):
	lsbByteArray = []
	dataString = ""
	secretFileName = ""
	lsbString = ""
	count = 0#iterator
	headerReceived=0#flags
	sizeReceived=0
	imageObj = dcimage.openFile(imagePath)
	pixels = imageObj.load()
	imgWidth, imgHeight = imageObj.size

	#cycle through each pixel
	for x in range(imgWidth):
		for y in range(imgHeight):
			r, g, b = pixels[x, y]
			#trim so we are dealing with only the least significant bit
			redPixel = str(bin(r)[2:].zfill(8))[7]
			greenPixel = str(bin(g)[2:].zfill(8))[7]
			bluePixel = str(bin(b)[2:].zfill(8))[7]
			secretBits = [redPixel, greenPixel, bluePixel]

			#for each of rgb
			for i in range(0,3):
				#check if our flags are set
				if (headerReceived == 0 or sizeReceived == 0):
					lsbString += secretBits[i]

					#verify each byte
					if len(lsbString) == 8:
						lsbByteArray.append(lsbString)

						#check if we have received a NULL byte
						if lsbString == "00000000":
							if headerReceived == 0:

								#convert the the bit array into an ascii String 
								#set flag when header and size was received
								fileName = ''.join(binascii.unhexlify('%x' % int(b,2)) for b in lsbByteArray[0:len(lsbByteArray) - 1])
								print "File name: " + str(fileName)
								headerReceived = 1
							elif sizeReceived == 0:
								fileSize = ''.join(binascii.unhexlify('%x' % int(b,2)) for b in lsbByteArray[0:len(lsbByteArray) - 1])
								print "File size: " + fileSize
								sizeReceived=1

							#reset the values
							lsbByteArray = []
						lsbString = ""

				#once headers received, resulting data is hidden data
				elif (headerReceived == 1 and sizeReceived == 1):
					if int(count) < int(fileSize):
						dataString += secretBits[i]#keep appending secret bits to the dataString until depleted
						count += 1
					else:
						#send to have hidden file created
						return dcimage.saveImage(outputFileName, dataString)
	
