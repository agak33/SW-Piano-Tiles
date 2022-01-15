from PianoTiles.ledStrip import LedStrip
import serial
import sqlite3
import pygame as pg
import time
import board
import RPi.GPIO as GPIO

SONGS_FOLDER = 'PianoTiles/songs'
FILE_EXTENSION = 'txt'

STRIP_NUM = 8
LED_PER_STRIP = 5

iterationTime = {
    'Easy'  : 2,
    'Middle': 1.5,
    'Hard'  : 0.75
}


class Game(object):
    def __init__(self, level: str, difficulty: str, color: str) -> None:
        self.level      = open(f'{SONGS_FOLDER}/{level}.{FILE_EXTENSION}')
        self.difficulty = difficulty
        self.time       = iterationTime[difficulty]
        self.color      = color
        self.points     = 0
        self.buttonPins = (18, 23, 24, 25, 12, 16, 20, 21)
        self.ledStrips  = []
        self.ser        = serial.Serial(port="/dev/ttyACM0", baudrate=9600)
        self.setup()

    def setup(self) -> None:
        pg.mixer.init(44100, -16, 1, 1024)
        pg.init()

        for btn in self.buttonPins:
            GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(channel=btn, egde=GPIO.RISING, callback=self.buttonCallback)
            pass

        self.ledStrips.append(
            LedStrip(ledNumTop=0 , ledCount=LED_PER_STRIP, direction=  1, note='C4', color=self.color, pin=18))
        self.ledStrips.append(
            LedStrip(ledNumTop=9 , ledCount=LED_PER_STRIP, direction= -1, note='D4', color=self.color, pin=23))
        self.ledStrips.append(
            LedStrip(ledNumTop=10, ledCount=LED_PER_STRIP, direction=  1, note='E4', color=self.color, pin=24))
        self.ledStrips.append(
            LedStrip(ledNumTop=19, ledCount=LED_PER_STRIP, direction= -1, note='F4', color=self.color, pin=25))
        self.ledStrips.append(
            LedStrip(ledNumTop=20, ledCount=LED_PER_STRIP, direction=  1, note='G4', color=self.color, pin=12))
        self.ledStrips.append(
            LedStrip(ledNumTop=29, ledCount=LED_PER_STRIP, direction= -1, note='A4', color=self.color, pin=16))
        self.ledStrips.append(
            LedStrip(ledNumTop=30, ledCount=LED_PER_STRIP, direction=  1, note='B4', color=self.color, pin=20))
        self.ledStrips.append(
            LedStrip(ledNumTop=39, ledCount=LED_PER_STRIP, direction= -1, note='C5', color=self.color, pin=21))

    def play(self) -> None:
        for note in self.level:
            note = note.strip()
            startTime = time.time()
            for index in range(len(self.ledStrips)):
                self.ledStrips[index].updateLedNumsColor()
                if self.ledStrips[index].noteName == note:
                    self.ledStrips[index].newLed()

                for led in self.ledStrips[index].ledNumsColor:
                    self.ser.write(f'{str(led.number).zfill(3)} '
                                   f'{str(led.color[0]).zfill(3)} '
                                   f'{str(led.color[1]).zfill(3)} '
                                   f'{str(led.color[2]).zfill(3)} \n'.encode('utf-8'))
                    # print(f'{str(led.number).zfill(3)} '
                    #       f'{str(led.color[0]).zfill(3)} '
                    #       f'{str(led.color[1]).zfill(3)} '
                    #       f'{str(led.color[2]).zfill(3)} \n'.encode('utf-8'))
            # self.buttonCallback(18)
            # self.buttonCallback(23)
            # self.buttonCallback(24)
            # self.buttonCallback(25)
            # self.buttonCallback(12)
            # self.buttonCallback(16)
            # self.buttonCallback(20)
            # self.buttonCallback(21)
            time.sleep(self.time - (time.time() - startTime))

    def buttonCallback(self, channel: int) -> None:
        self.ledStrips[ self.ledStrips.index(channel) ].playSound()



