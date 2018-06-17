from random import randint, random

from PyQt5.QtCore import QRunnable, pyqtSlot

import serial
import time

from worker_signals import WorkerSignals

SENSITIVITY = 700
PORT = 'com3'
flag = True


def check_signal(value):
    if value < SENSITIVITY:
        return True
    return False


def get_test_string():
    return "{} {}".format(randint(1, 3), random())


class Arduino(QRunnable):
    def __init__(self, *args, **kwargs):
        super(Arduino, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        try:
            self.arduino_serial = serial.Serial(PORT, 9600)
            time.sleep(5)
        except:
            print('Not connection')
            return

    @pyqtSlot()
    def run(self):
        while True:
            str = self.arduino_serial.readline()
            # str = get_test_string()

            numb, value = str.split()
            numb, value = int(numb), float(value)
            numb = 1
            if check_signal(value):
                self.signals.result.emit(numb)
            else:
                self.signals.finished.emit()
            time.sleep(0.3)
