import random


def getRandomColor():
    return random.choice([
        (255,   0,   0),        # red
        (200,  70,   0),        # orange
        (150, 150,   0),        # yellow
        (  0, 255,   0),        # green
        (  0, 100, 200),        # blue
        (  0,   0, 255),        # navy blue
        ( 70,   0, 200)         # purple
    ])


class Led(object):
    def __init__(self, number: int, color: str):
        colors = {
            'White'     : (100, 100, 100),
            'Red'       : (255, 0, 0),
            'Green'     : (0, 255, 0),
            'Blue'      : (0, 0, 255),
            'Yellow'    : (150, 150, 0),
            'Magenta'   : (150, 0, 150),
            'Cyan'      : (0, 150, 150),
            'RAINBOW MODE'   : getRandomColor()
        }
        self.number = number
        self.color  = colors[color]

    def __add__(self, other: int):
        self.number += other
        return self

    def __eq__(self, other: int):
        return self.number == other

    def __repr__(self):
        return f'Led number {self.number}, color: {self.color}'
