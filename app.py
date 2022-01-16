from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QSize, pyqtSignal, pyqtSlot, QObject
from PyQt5.QtGui import QFontDatabase, QFont, QIcon
from PyQt5.QtWidgets import QWidget, QTableWidgetItem

from GUI.setup import *
from PianoTiles.game import Game
from database.database import Database


class App(QObject):
    gameOverSignal = pyqtSignal()

    def __init__(self) -> None:
        super(App, self).__init__()
        self.app              = QtWidgets.QApplication([])
        self.app.aboutToQuit.connect(self.quit)
        self.window           = QtWidgets.QMainWindow()
        self.screen           = QtWidgets.QWidget()
        self.database         = Database()
        self.gameOverSignal.connect(self.gameOver)

        self.difficultyLevels = ['Easy', 'Middle', 'Hard']
        self.currDifficulty   = 0

        self.levelsTitles     = ['angry birds', 'rudolph the red nosed raindeer', 'you\'ve got a friend in me']
        self.currLevel        = self.levelsTitles[0]
        self.points           = 0

        self.ledColors        = ['White', 'Blue', 'Red', 'Green', 'Yellow', 'Magenta', 'Cyan', 'RAINBOW MODE']
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

    def level(self, value: str) -> None:
        self.currLevel = value

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
        self.screen.chooseLevelBox.currentTextChanged.connect(self.level)
        self.screen.playButton.clicked.connect(self.play)

    def ranking(self) -> None:  
        self.loadScreen(f'{UI_FOLDER_PATH}/{UI_RANKING}')
        self.screen.rankingTable.setHorizontalHeaderLabels(('Points', 'Song', 'Player'))
        results = self.database.getRanking()

        self.screen.rankingTable.setRowCount(len(results))

        for rowNum, result in enumerate(results):
            self.screen.rankingTable.setItem(rowNum, 0, QTableWidgetItem(f'{result[2]}'))
            self.screen.rankingTable.setItem(rowNum, 1, QTableWidgetItem(f'{result[0]}'))
            self.screen.rankingTable.setItem(rowNum, 2, QTableWidgetItem(f'{result[1]}'))

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

    def play(self) -> None:
        self.window.close()
        print(f'Chosen level: {self.difficultyLevels[self.currDifficulty]} {self.currLevel}')
        print(f'Led color: {self.ledColors[self.currLedColor]}')
        game = Game(self.currLevel, self.difficultyLevels[self.currDifficulty], self.ledColors[self.currLedColor])
        self.points = game.play()
        self.gameOverSignal.emit()

    def gameOver(self):
        self.loadScreen(f'{UI_FOLDER_PATH}/{UI_GAMEOVER}')
        self.screen.pointsLabel.setText(f'{self.points}')
        self.screen.gameTitleLabel.setText(f'{self.currLevel}')

        self.screen.cancelButton.clicked.connect(self.mainMenu)
        self.screen.saveButton.clicked.connect(
            lambda: self.saveResults(self.points, self.currLevel, self.screen.nameField.text())
        )
        self.window.show()

    def saveResults(self, points: int, selectedLevel: str, name: str):
        self.database.saveGame(selectedLevel, name, points)
        self.mainMenu()

    def quit(self) -> None:
        self.database.close()
        self.window.close()
