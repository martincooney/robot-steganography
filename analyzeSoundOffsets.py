#!/usr/bin/env python3


print('----------------------------------------------------------------')
print('-             Baxter speech onset steganography demo           -')
print('-              MAR 2021, Halmstad U., Martin Cooney            -')
print('----------------------------------------------------------------')


print("\nReading in speech onset data for steganographic and normal messages:")
print("20 samples were obtained, 10 per class")
print("Half are used for training, and half for testing; each run contains 10 speech events.")

numberOfWords=10 

f= open("audiolog_hidden.txt", "r")
l2=f.read()
f.close()
l=l2.split()

numberOfSamplesHidden= (int)(len(l)/numberOfWords)
trainingHidden = l[0:(int)(len(l)/2)]
testHidden = l[(int)(len(l)/2): len(l)]

f= open("audiolog_normal.txt", "r")
l2=f.read()
f.close()
l=l2.split()

numberOfSamplesNormal=(int)(len(l)/numberOfWords)
trainingNormal = l[0: (int)(len(l)/2)]
testNormal = l[(int)(len(l)/2): len(l)]


print("Task 1: Classify samples as steganographic or normal")
print("Automatically find a threshold on total time")

#we use a very simple approach: given the speech onset delays, a steganographic sample takes more overall time
wordIndex = 9
myAveHidden=0
min=9999
max=-99999
for sampleIndex in range(int(numberOfSamplesHidden/2)):
	#print("sampleIndex", sampleIndex)
	#print("looking for index", sampleIndex*numberOfWords + wordIndex)
	currentValue=float(trainingHidden[sampleIndex*numberOfWords + wordIndex])
	myAveHidden += currentValue
	if(min > currentValue):
		min= currentValue
	if(max < currentValue):
		max= currentValue
myAveHidden/=(float(numberOfSamplesHidden/2))
print("Stats for hidden speech")
#print("Word", wordIndex)
print("ave", myAveHidden)
print("max", max)					
print("min", min)
print("range", max-min)


myAveNormal=0
min=9999
max=-99999
for sampleIndex in range(int(numberOfSamplesNormal/2)):
	#print("sampleIndex", sampleIndex)
	#print("looking for index", sampleIndex*numberOfWords + wordIndex)
	currentValue=float(trainingNormal[sampleIndex*numberOfWords + wordIndex])
	myAveNormal += currentValue
	if(min > currentValue):
		min= currentValue
	if(max < currentValue):
		max= currentValue
myAveNormal/=(float(numberOfSamplesNormal/2))
print("Stats for normal speech")
#print("Word", wordIndex)
print("ave", myAveNormal)
print("max", max)					
print("min", min)
print("range", max-min)


timeThreshold = myAveNormal +  (myAveHidden - myAveNormal)/2.0
print("Check if the total time is greater or less than the detected threshold:", timeThreshold)

correctlyClassified = 0

for sampleIndex in range(int(numberOfSamplesHidden/2)):
	currentValue=float(trainingHidden[sampleIndex*numberOfWords + wordIndex])
	if(timeThreshold < currentValue):
		correctlyClassified+=1

for sampleIndex in range(int(numberOfSamplesNormal/2)):
	currentValue=float(testNormal[sampleIndex*numberOfWords + wordIndex])
	if(timeThreshold > currentValue):
		correctlyClassified+=1

numberOfTestSamples = numberOfSamplesHidden/2 + numberOfSamplesNormal/2
accuracy = (correctlyClassified/numberOfTestSamples) * 100
print("Classification accuracy:", accuracy )


#Task 2: detect the hidden message
#again, we use a simple approach: we subtract the normal averages from steganographic times, then classify the differences between speech event onsets
#as dots, dashes, or nothing
#as a simple example, we just use the average steganographic times...

#get averages for all in the hidden training set
aves=[]
for wordIndex in range(numberOfWords):
	myAveHidden=0
	for sampleIndex in range(int(numberOfSamplesHidden/2)):
		currentValue=float(trainingHidden[sampleIndex*numberOfWords + wordIndex])
		myAveHidden += currentValue
	myAveHidden/=(float(numberOfSamplesHidden/2))
	aves.append(myAveHidden)

#get averages for all in the normal training set
avesNormal=[]
diffs2=[]
for wordIndex in range(numberOfWords):
	myAveNormal=0
	for sampleIndex in range(int(numberOfSamplesNormal/2)):
		currentValue=float(trainingNormal[sampleIndex*numberOfWords + wordIndex])
		myAveNormal += currentValue
	myAveNormal/=(float(numberOfSamplesNormal/2))
	avesNormal.append(myAveNormal)

#get the differences
for wordIndex in range(0, len(avesNormal)): 
	diff= aves[wordIndex] - avesNormal[wordIndex]
	diffs2.append(diff)

#decode the delays
dashes=[]
for wordIndex in range(1, len(diffs2)):
	diff= float(diffs2[wordIndex]) - float(diffs2[wordIndex-1]) 
	if diff > 0.05 and diff <= 0.15:         #dot was arbitrarily set here to around 100ms
		dashes.append(0)
	elif diff > 0.15:                        #dash was arbitrarily set here to around 200ms (note that usually dash is 3x dot, and there are spaces, etc)
		dashes.append(1)

#assume last signal is repeated as the way we have set up our system; if we don't want to do this, the robot can just add one extra word at the end
dashes.append(dashes[len(dashes)-1])
print("Encoded sequence:", dashes)

print("The hidden message is:")
if(	(dashes[0]==0 and dashes[1]==0 and dashes[2]==0) and
	(dashes[3]==1 and dashes[4]==1 and dashes[5]==1) and
	(dashes[6]==0 and dashes[7]==0 and dashes[8]==0)):
	print("SOS")
else:
	print("not SOS")


