import sys, os, argparse, binascii, array
import dcutils
from PIL import Image

#Command Line Argument Parser
parser = argparse.ArgumentParser(description='Steganography Using LSB Method')
parser.add_argument('-m', '--mode', dest='mode', help="Use an 'e' for encoding an image or a 'd' for decoding.", required=True)
parser.add_argument('-i', '--image', dest='image', help='image that will be manipulated', required = True)
parser.add_argument('-s', '--secret', dest='secretData', help='path to secret file')
parser.add_argument('-o', '--output', dest='outputFile', help='file name of outputFile', required=True)
parser.add_argument('-p', '--password', dest='password', help='password to encrypt / decrypt file', required=True)

#parsing arguments
args = parser.parse_args()
password = args.password
image = args.image
secretData = args.secretData
outputFile = args.outputFile

#check if cover image is big enough to hide secret data
def compareFiles():
    #open cover image
	image = Image.open(args.image)
    #get width and height of cover image
	width, height = image.size
    #get storable bits size in cover image
	storableBits = width * height *3	#3 bits in a pixel
    #get secret data size in bits
	secretFileSize = os.path.getsize(args.secretData) * 8  #in bits

    #if cover image has enough size of bits to hide secret data return True
	if storableBits > secretFileSize:
		return 1

    #cover image doesn't have enough space to hide secret data. Print error message.
	else:
		print "\nCover image is not big enough"
		print "Cover image size: "+str(storableBits)
		print "Secret file size: "+str(secretFileSize)
        #program exit
        exit()

def main():
    #encode mode
	if args.mode == "e":
		if compareFiles() == 1:
			dcutils.encode(image, secretData, outputFile, password)

    #decode mode
	elif args.mode == "d":
		dcutils.decode(image, outputFile, password)


if __name__ == '__main__':
	main()
