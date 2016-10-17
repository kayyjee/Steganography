import sys, os, argparse, binascii, array
import utils

from PIL import Image

#Command Line Argument Parser
parser = argparse.ArgumentParser(description='Steganography Using LSB Method')
parser.add_argument('-m', '--mode', dest='mode', help="Use an 'e' for encoding an image or a 'd' for decoding.", required=True)
parser.add_argument('-i', '--image', dest='image', help='image that will be manipulated', required = True)
parser.add_argument('-s', '--secret', dest='secretData', help='path to secret file')
parser.add_argument('-o', '--output', dest='outputFile', help='file name of outputFile', required=True)
parser.add_argument('-p', '--password', dest='password', help='password to encrypt / decrypt file', required=True)

args = parser.parse_args()

password = args.password
image = args.image
secretData = args.secretData
outputFile = args.outputFile
	



def compareFiles():

	image = Image.open(args.image)
	width, height = image.size
	storableBits = width * height *3	#3 bits in a pixel
	secretFileSize = os.path.getsize(args.secretData) * 8  #in bits

	if storableBits > secretFileSize:
		return 1

	else:
		print "\nCover image is not big enough"
		print "Cover image size: "+str(storableBits)
		print "Secret file size: "+str(secretFileSize)
		exit()





def main():
	if args.mode == "e":
		if compareFiles() == 1:
			utils.encode(image, secretData, outputFile, password)
			

	elif args.mode == "d":
		utils.decode(image, outputFile, password)
		

if __name__ == '__main__':
	main()
	
	
