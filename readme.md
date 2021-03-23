Robot Steganography

Basic Concept

We believe robots will be able to help vulnerable people via "steganography"--i.e., sending hidden messages--to communicate, warn of threats, and get help.
Details are provided in a paper submitted to RO-MAN 2021 and video (links will be added later).
To help others to get started in this area, the author is making available a few goodies.

Content (requirements, files)

Requirements: Python 3 was used, with the Baxter robot.

Files:

motion_steganography.py:
Just run it once to see how it works, with some default settings:
python motion_steganography.py
It hides a message in a motion file for the robot Baxter, using a very common and simple steganography method (LSB with ASCII).
Once you get the idea, feel free to tape your own motions for Baxter and change the default settings, like the source/target filenames and the hidden message, specified at the top of the code.

analyzeSoundOffsets.py:
This shows an example of steganalysis for a message "SOS" encoded into our Baxter robot's speech delays using "pseudo"-Morse code.
The speech onsets were automatically detected using a microphone and these data are processed.
This example shows (1) detecting if a speech sample had a hidden message or not and (2) decoding the message.
Data are stored in audiolog_hidden.txt and audiolog_normal.txt

examples:
This folder contains examples of WAV files and PNG images which have messages hidden in them (LSB/ASCII). There is much code on Google that can do this.

Other code will probably follow...

(Note: This code was written using the author's setup described above for research purposes; the author cannot help with getting it to work on the reader's system.)

Licenses

For this author's code and dataset, the MIT license applies:

Copyright 2021 Martin Cooney

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated dataset and documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
