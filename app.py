from os import set_blocking
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFontDatabase, QFont, QIcon
from GUI.setup import *


class App(object):
    def __init__(self) -> None:
        self.app              = QtWidgets.QApplication([])
        self.window           = QtWidgets.QMainWindow()
        self.screen           = QtWidgets.QWidget()

        self.difficultyLevels = ['Easy', 'Middle', 'Hard']
        self.currDifficulty   = 0

        self.levelsTitles     = ['OPCJA 1', 'OPCJA 2', 'OPCJA 3']

        self.ledColors        = ['White', 'Blue', 'Red', 'Green', 'RAINBOW MODE']
        self.currLedColor     = 0

        self.setupMainWindow()
        self.mainMenu()

    def setupMainWindow(self) -> None:
        uic.loadUi(f'{UI_FOLDER_PATH}/{UI_MAIN_WINDOW}')
        QFontDatabase.addApplicationFont(FONT_PATH)
        self.window.statusBar().setSizeGripEnabled(False)
        self.window.show()
        self.window.setFixedSize(QSize(SIZE_WIDTH, SIZE_HEIGHT))

    def loadScreen(self, path: str) -> None:
        self.screen = QtWidgets.QWidget()
        uic.loadUi(path, self.screen)
        self.screen.setFont(QFont("PatrickHandSC"))
        self.window.setCentralWidget(self.screen)

    def mainMenu(self) -> None:
        self.loadScreen(f'{UI_FOLDER_PATH}/{UI_MAIN_MENU}')

        self.screen.startGameButton.clicked.connect(self.startGame)
        self.screen.rankingButton.clicked.connect(self.ranking)
        self.screen.settingsButton.clicked.connect(self.settings)
        self.screen.quitButton.clicked.connect(self.quit)

    def difficultyIndex(self, direction: int) -> int:
        self.currDifficulty += direction
        if self.currDifficulty < 0:
            self.currDifficulty = len(self.difficultyLevels) - 1
        elif self.currDifficulty >= len(self.difficultyLevels):
            self.currDifficulty = 0
        return self.currDifficulty

    def startGame(self) -> None:
        self.loadScreen(f'{UI_FOLDER_PATH}/{UI_START_GAME}')        

        self.screen.difficultyLabel.setText(self.difficultyLevels[self.currDifficulty])
        self.screen.chooseLevelBox.addItems(self.levelsTitles)
        self.screen.difficultyMoreButton.setIcon(QIcon(NEXT_ICON_PATH))
        self.screen.difficultyLessButton.setIcon(QIcon(PREV_ICON_PATH))

        self.screen.cancelButton.clicked.connect(self.mainMenu)
        self.screen.difficultyMoreButton.clicked.connect(
            lambda: self.screen.difficultyLabel.setText(
                self.difficultyLevels[self.difficultyIndex(1)]
            )
        )
        self.screen.difficultyLessButton.clicked.connect(
            lambda: self.screen.difficultyLabel.setText(
                self.difficultyLevels[self.difficultyIndex(-1)]
            )
        )
        self.screen.playButton.clicked.connect(
            lambda: self.play(self.screen.chooseLevelBox.currentText())
        )
        

    def ranking(self) -> None:  
        self.loadScreen(f'{UI_FOLDER_PATH}/{UI_RANKING}')

        self.screen.mainMenuButton.clicked.connect(self.mainMenu)

    def ledColorIndex(self, direction: int) -> int:
        self.currLedColor += direction
        if self.currLedColor < 0:
            self.currLedColor = len(self.ledColors) - 1
        elif self.currLedColor >= len(self.ledColors):
            self.currLedColor = 0
        return self.currLedColor

    def settings(self) -> None:
        self.loadScreen(f'{UI_FOLDER_PATH}/{UI_SETTINGS}')

        self.screen.colorPrevButton.setIcon(QIcon(PREV_ICON_PATH))
        self.screen.colorNextButton.setIcon(QIcon(NEXT_ICON_PATH))
        self.screen.ledColorLabel.setText(self.ledColors[self.currLedColor])

        self.screen.mainMenuButton.clicked.connect(self.mainMenu)
        self.screen.colorNextButton.clicked.connect(
            lambda: self.screen.ledColorLabel.setText(self.ledColors[self.ledColorIndex(1)])
        )
        self.screen.colorPrevButton.clicked.connect(
            lambda: self.screen.ledColorLabel.setText(self.ledColors[self.ledColorIndex(-1)])
        )

    def play(self, selectedLevel) -> None:
        print(f'Chosen level: {self.difficultyLevels[self.currDifficulty]} {selectedLevel}')
        print(f'Led color: {self.ledColors[self.currLedColor]}')

    def quit(self) -> None:
        self.window.close()
