from collections import defaultdict
from functools import partial

from PyQt5.QtCore import QThreadPool

from arduino import Arduino
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QCheckBox, QLabel

from timer import Timer

NUMB_SENSOR = 3
DIALOG_X = 200
DIALOG_Y = 40
DIALOG_STEP = 60
DIALOG_W = 200
DIALOG_H = 45
SWITCH_X = 10


class Desktop(QWidget):

    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        self.i = DIALOG_Y
        self.dialogs = []
        self.switches = []
        self.button = QPushButton("Cигнализация", self)
        self.timer_labels = []
        self.timer = defaultdict(int)
        self.cancel_buttons = []

        self.initUI()

    def initUI(self):
        self.create_window()
        self.createDialogs()
        self.create_switches()
        # self.create_button()
        self.createTimerLabel()
        self.create_cancel_button()

        self.show()
        self.logic()

    def update_timer(self, kwargs):
        sensor = kwargs['sensor'] - 1
        t = kwargs['t']
        if self.timer[sensor] == 99:
            return
        timer_str = f"00:{t}"
        self.timer_labels[sensor].setText(timer_str)
        if t == 0:
            self.start_extinction(sensor)

    def start_extinction(self, n):
        self.timer_labels[n].setStyleSheet("QLabel { color: green; }")
        self.timer_labels[n].setText("Начато тушение")

    def set_timer(self, n):
        if self.timer[n] != 0:
            return
        else:
            self.timer[n] = 30
        timer = Timer(self.update_timer, sensor=n)
        timer.signals.result.connect(self.update_timer)
        self.threadpool.start(timer)

    def start_warning(self, n):
        self.setText(n - 1, "Пожар!")
        self.set_timer(n)

    def idle(self):
        pass

    def logic(self):
        arduino = Arduino()
        arduino.signals.result.connect(self.start_warning)
        arduino.signals.finished.connect(self.idle)
        self.threadpool.start(arduino)

    def create_window(self):
        self.resize(900, 600)
        self.move(1500, 10)
        self.setWindowTitle('Warm Detector')

    def createDialogs(self):
        for i in range(NUMB_SENSOR):
            self.dialogs.append(QLineEdit(self))

        self.i = DIALOG_Y
        for dialog in self.dialogs:
            dialog.move(DIALOG_X, self.i)
            dialog.resize(DIALOG_W, DIALOG_H)
            self.i += DIALOG_STEP

    def create_switches(self):
        for i in range(NUMB_SENSOR):
            self.switches.append(QCheckBox("Датчик " + str(i + 1), self))

        self.i = DIALOG_Y
        for switch in self.switches:
            switch.move(SWITCH_X, self.i)
            switch.setStyleSheet("QCheckBox::indicator { width: 30px; height: 30px;}")
            switch.toggle()
            self.i += DIALOG_STEP

    def create_button(self):
        self.button.setCheckable(True)
        self.button.move(SWITCH_X, self.i)

    def createTimerLabel(self):
        for i in range(NUMB_SENSOR):
            self.timer_labels.append(QLabel('', self))

        i = 40
        for label in self.timer_labels:
            label.move(500, i)
            label.resize(DIALOG_W, DIALOG_H)
            label.setStyleSheet("QLabel { color: red; }")
            i += 60

    def cancel_timer(self, *args, **kwargs):
        n = args[0]
        self.timer_labels[n].setText("Тушение отменено")
        self.timer_labels[n].setStyleSheet("QLabel { color: yellow; }")
        self.timer[n] = 99

    def create_cancel_button(self):
        for i in range(NUMB_SENSOR):
            btn = QPushButton('Отмена', self)
            btn.clicked.connect(partial(self.cancel_timer, i))
            self.cancel_buttons.append(btn)

        i = 40
        for n, btn in enumerate(self.cancel_buttons):
            btn.move(650, i)
            btn.resize(DIALOG_W, DIALOG_H)
            btn.setStyleSheet("QLabel { color: red; }")

            i += 60

    def clickButton(self, bool):
        self.button.setCheckable(bool)

    def getSwitch(self, n):
        return self.switches[n].isChecked()

    def getButton(self):
        return self.button.isChecked()

    def setText(self, n, text):
        self.dialogs[n].setText(text)
