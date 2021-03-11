import os
import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QSpinBox, QLineEdit, QLabel, QFileDialog
from start_window import Ui_MainWindow

class StartWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # self.players_number_spinBox = QSpinBox()
        # uic.loadUi('start_window.ui', self)
        self.setupUi(self)
        self.players_names = [self.player1_name, self.player2_name,
                              self.player3_name, self.player4_name]
        self.players_number_spinBox.textChanged.connect(self.players_number_change)
        self.open_folder_Btn.clicked.connect(self.open_folder)
        self.start_game_Btn.clicked.connect(self.start_game)

    def players_number_change(self):
        # self.label_2 = QLabel()
        # self.player2_name = QLineEdit()
        self.label_2.setEnabled(True)
        self.player2_name.setEnabled(True)
        self.label_3.setEnabled(True)
        self.player3_name.setEnabled(True)
        self.label_4.setEnabled(True)
        self.player4_name.setEnabled(True)
        if int(self.players_number_spinBox.text()) == 1:
            self.label_2.setDisabled(True)
            self.player2_name.setDisabled(True)
            self.label_3.setDisabled(True)
            self.player3_name.setDisabled(True)
            self.label_4.setDisabled(True)
            self.player4_name.setDisabled(True)
        elif int(self.players_number_spinBox.text()) == 3:
            self.label_4.setDisabled(True)
            self.player4_name.setDisabled(True)
        elif int(self.players_number_spinBox.text()) == 2:
            self.label_3.setDisabled(True)
            self.player3_name.setDisabled(True)
            self.label_4.setDisabled(True)
            self.player4_name.setDisabled(True)
        self.update()

    def open_folder(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        dialog.setOption(QFileDialog.ShowDirsOnly)
        if dialog.exec():
            self.folderName_Edit.setText(dialog.selectedFiles()[0])

    def start_game(self):
        import json
        game_params = {
            'players_number': self.players_number_spinBox.text(),
            'player1_name': self.player1_name.text(),
            'player2_name': self.player2_name.text(),
            'player3_name': self.player3_name.text(),
            'player4_name': self.player4_name.text(),
            'folder':  self.folderName_Edit.text()
        }
        print(game_params)
        with open(self.folderName_Edit.text()+'\\game.json', 'w') as file:
            json.dump(game_params, file, ensure_ascii=False, indent=2)



def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def main():
    app = QApplication(sys.argv)
    ex = StartWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())

main()