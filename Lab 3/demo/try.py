import time
import board
import busio
import adafruit_mpu6050
import json
import socket

import signal
import sys
from queue import Queue

from vosk import Model, KaldiRecognizer
import sys
import os
import wave
 

print('\n\n\n\nSay out the password\n\n\n\n\n') 
i2c = busio.I2C(board.SCL, board.SDA)
mpu = adafruit_mpu6050.MPU6050(i2c)

if not os.path.exists("model"):
    print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
    exit (1)

wf = wave.open(sys.argv[1], "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print ("Audio file must be WAV format mono PCM.")
    exit (1)

model = Model("model")
# You can also specify the possible word list
rec = KaldiRecognizer(model, wf.getframerate(), "zero oh one two three four five six seven eight nine [unk]")

print('\n\n\n\nhake the box\n\n\n\n')

while True:
    data = wf.readframes(6000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        if 'one' in rec.PartialResult() and 'two' in rec.PartialResult() and 'three' in rec.PartialResult() and abs(max(mpu.acceleration)) > 10:
            print(rec.PartialResult())
            print(mpu.acceleration)
            print('You opened the box')
            break
    else:
        if 'one' in rec.PartialResult() and 'two' in rec.PartialResult() and 'three' in rec.PartialResult() and abs(max(mpu.acceleration)) > 10:
            print('You opened the box')
            print(rec.PartialResult())
            print(mpu.acceleration)
            break

# print(rec.FinalResult())




