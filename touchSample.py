import sys
import time
import pygame
import Adafruit_MPR121.MPR121 as MPR121

cap1 = MPR121.MPR121()
cap2 = MPR121.MPR121()
pygame.mixer.init()
pygame.mixer.set_num_channels(24)
soundFiles = [[
        'moods', 'coralreef', 'birdsong', 'thunder',
        'moods2', 'birdsong', 'stones', 'birdsong',
        'process', 'navy', 'godrevy', 'stream'
    ],
    [
        'noelectric', 'quarryfields', 'lochness', 'stream',
        'birdsong', 'allotment', 'imaginaryflower', 'porthleven',
        ' ', ' ', ' ', ' '
    ]
]

print('Loaded Sounds')
if not cap1.begin( 0x5a ):
    print('Error initializing MPR121 No1. Check your wiring!')
    sys.exit(1)
if not cap2.begin( 0x5b ):
    print('Error initializing MPR121 No2. Check your wiring!')
    sys.exit(1)
print('Initialised Touch boards')

def handleSound(pin, board, trigger):
    channelNo = pin + (board * 12)
    channel = pygame.mixer.Channel(channelNo)
    isBusy = channel.get_busy()
    soundFile = soundFiles[board][pin]

    if trigger == -1 and isBusy:
        print('stop' + str(i) + soundFile)
        channel.stop()
    if trigger == 1 and not isBusy:
        print('Play' + str(i) + soundFile)
        channel.set_volume(1)
        channel.play(pygame.mixer.Sound('sounds/' + soundFile +'.wav'))

def checkPin(i, current_touched, last_touched):
    pin_bit = 1 << i
    # First check if transitioned from not touched to touched.
    if current_touched & pin_bit and not last_touched & pin_bit:
        return 1;
    if not current_touched & pin_bit and last_touched & pin_bit:
        return -1;
    return 0;

last_touched_1 = cap1.touched()
last_touched_2 = cap2.touched()

while True:
    current_touched_1 = cap1.touched()
    current_touched_2 = cap2.touched()
    for i in range(12):
	pin1 =  checkPin(i, current_touched_1, last_touched_1)
	if 0 != pin1:
            handleSound(i, 0, pin1)
            print('1: ' + str(i) + ': ' + str(pin1))
	pin2 =  checkPin(i, current_touched_2, last_touched_2)
	if 0 != pin2:
            print('2: ' + str(i) + ': ' + str(pin2))
            handleSound(i, 1, pin2)

    last_touched_1 = current_touched_1
    last_touched_2 = current_touched_2
    time.sleep(0.1)


