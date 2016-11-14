import os, sys, binascii, array
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

    #get the file name in binary
	for bits in secretData:
		binName += format(ord(bits), 'b').zfill(8)#convert the file name to binary

    #get the file data in binary
	fileData = bytearray(open(secretData, 'rb').read())#opens the binary file in read or write mode
	for bits in fileData:
		binDataString += bin(bits)[2:].zfill(8)#convert the file data to binary

    #get the number od bits of the file in binary
	dataSize = list(str(len(binDataString)))#data size as a list of each int

    #convert the array of decimal numbers into a bit string
	for bits in dataSize:
		binDataSize += format(ord(bits), 'b').zfill(8)#convert the data size to binary

    #assemble string with NULL delimiters
	bitString = binName+nullDelimiter+binDataSize+nullDelimiter+binDataString

	return bitString

#converts the binary values for rgb into decimal
def getPixel(binRGB):
	rgbDecimalArray = []

	for col in binRGB:
		rgbDecimalArray.append(int(''.join(str(b) for b in col), 2))

    #return the rgb value of the pixel in decimal
    return (rgbDecimalArray[0], rgbDecimalArray[1], rgbDecimalArray[2])

#save the datastring with file filename
def saveImage(fileName, dataString):
	secretByteStrings = []

    #convert bit string into array of bytes in decimal format
	for i in range (0, len(dataString)/8):
		secretByteStrings.append(int(dataString[i*8:(i+1) * 8], 2))
		dataString
	print secretByteStrings
	secretByteString = array.array('B', secretByteStrings).tostring()
	secretData = bytearray(secretByteString)
	secretFile = open(str(fileName), 'w')
	secretFile.write(secretData)


def openFile(imagePath):
	return Image.open(imagePath).convert('RGB')
