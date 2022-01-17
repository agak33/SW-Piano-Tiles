import pygame as pg
from PianoTiles.led import Led
import time

NOTES_FOLDER = 'PianoTiles/sounds'


class LedStrip(object):
    def __init__(self, ledNumTop: int, ledCount: int, direction: int, note: str, color: str, pin: int):
        self.ledNumTop       = ledNumTop
        self.ledNumBottom    = ledNumTop + ((ledCount - 1) * direction)
        self.direction       = direction
        self.note            = pg.mixer.Sound(f'{NOTES_FOLDER}/{note}.wav')
        self.noteName        = note
        self.color           = color
        self.pinNumber       = pin
        self.ledNumsColor    = []
        self.soundPlayed     = False

    def __eq__(self, other: int):
        return self.pinNumber == other

    def newLed(self) -> None:
        self.ledNumsColor.append(Led(self.ledNumTop, self.color))

    def updateLedNumsColor(self) -> None:
        ledNumsColor = []
        for led in self.ledNumsColor:
            newLedNum = led + self.direction
            if      (self.ledNumTop     <= newLedNum.number <= self.ledNumBottom) or \
                    (self.ledNumBottom  <= newLedNum.number <= self.ledNumTop):
                ledNumsColor.append(newLedNum)
        self.soundPlayed = False
        self.ledNumsColor = ledNumsColor

    def playSound(self) -> None:
        if self.ledNumBottom in self.ledNumsColor and not self.soundPlayed:
            self.note.play()
            self.soundPlayed = True
            time.sleep(0.25)

    def check(self):
        return self.ledNumBottom in self.ledNumsColor

    def gameOver(self) -> bool:
        if self.ledNumBottom in self.ledNumsColor and not self.soundPlayed:
            return True
        return False


