#!/usr/bin/env python3

import struct
import math
from codecs import decode

sourceFileName = "stegMotion1.txt"
targetFileName = "stegMotion1_embedded.txt"
messageToHide = "SOS! I am out of coffeee!"

def float_to_bin32(num):
	return format(struct.unpack('!I', struct.pack('!f', num))[0], '032b')

def bin_to_float32(binary):
	return struct.unpack('!f',struct.pack('!I', int(binary, 2)))[0]

def stringToBinaryString(data):
	newData = []
	for i in data:
		newData.append(format(ord(i), '08b'))
	allTogether = ''.join(newData)
	return allTogether  

def changeLastBit(aFloat, desiredLSB):
	bitString= float_to_bin32(aFloat)
	list1 = list(bitString)
	list1[31] = desiredLSB
	bitString = ''.join(list1)
	newFloat = bin_to_float32(bitString)
	return newFloat

def getLastBit(aFloat):
	bitString = float_to_bin32(aFloat)
	return bitString[31]

def encodeMotion():

	print("")
	print("")
	print("----------------------------ENCODING----------------------------")

	#read in a motion file (carrier)
	f = open(sourceFileName, "r")
	l = f.read()
	f.close() 

	#display some basic information
	myMessageBinary = stringToBinaryString(messageToHide) 
	howManyRowsNeededForMessage= math.ceil(len(myMessageBinary)/6.0)
	numRowsAvailable = (len(l)-1)
	print("Source file:", sourceFileName)
	print("Target file:", targetFileName)
	print("Message to encode:", messageToHide)
	print("Message in binary:", myMessageBinary)
	print("Message length:", len(myMessageBinary))
	print("Number of rows needed:", howManyRowsNeededForMessage)
	print("Number of rows available:", numRowsAvailable)
	if(howManyRowsNeededForMessage > numRowsAvailable):
		print("Not enough rows in motion file... Reduce message size or record a longer motion")
		exit()

	#insert message into motion data
	newL2 = l.split() # break the motion file data into rows 
	insertionCount=0
	for aRowIndex in range(1, howManyRowsNeededForMessage+1): #skip first row of text
		aRow= newL2[aRowIndex].split(",")
		for floatIndex in range(6):
			if(insertionCount < len(myMessageBinary)):
				aRow[8+floatIndex] = str(changeLastBit(float(aRow[8+floatIndex]), myMessageBinary[insertionCount])) 
				insertionCount+=1
		aRow[14] = str(changeLastBit(float(aRow[14]), '1'))
		newL2[aRowIndex]= ','.join(aRow)

	#add stop bit
	aRow= newL2[howManyRowsNeededForMessage+1].split(",") #next row
	aRow[14] = str(changeLastBit(float(aRow[14]), '0'))
	newL2[howManyRowsNeededForMessage+1]= ','.join(aRow)

	#write to a new motion file	
	f2 = open(targetFileName,'w')
	for aRowIndex in range(len(newL2)):
		f2.write(newL2[aRowIndex])
		f2.write("\n")
	f2.close() 


def decodeMotion():

	print("")
	print("----------------------------DECODING----------------------------")

	#read in a motion file (carrier)
	f = open(targetFileName, "r")
	l = f.read()
	f.close() 
	newL2 = l.split() # break the motion file data into rows 

	#now, decode the message
	#look at each continue bit in row position 14
	#if 1, add six values to our array/list
	#if 0, stop

	decodedMessageBinary = []	
	for aRowIndex in range(1, len(newL2)):
		aRow= newL2[aRowIndex].split(",")
		lastBit= getLastBit(float(aRow[14]))
		if (lastBit[0]=="1"):
			for floatIndex in range (6):
				decodedMessageBinary.append(getLastBit(float(aRow[8+floatIndex])))
		else:
			break
	decodedMessageBinaryString= ''.join(decodedMessageBinary)

	#remove excess bits so we only get whole bytes
	numberOfBitsToKeep = int(len(decodedMessageBinaryString)/8) * 8
	decodedMessageBinaryString2 = decodedMessageBinaryString[0:numberOfBitsToKeep]

	#convert from binary to ASCII
	myNewString = '0b' + decodedMessageBinaryString2
	n = int(myNewString, 2) 
	print("Decoded message:", n.to_bytes((n.bit_length() + 7) // 8, 'big').decode())


def main():

	print('----------------------------------------------------------------')
	print('-                 Baxter motion steganography demo             -')
	print('-                  MAR 2021, Halmstad U., Martin               -')
	print('----------------------------------------------------------------')

	encodeMotion()
	decodeMotion()


if __name__ == '__main__' :
	main()





