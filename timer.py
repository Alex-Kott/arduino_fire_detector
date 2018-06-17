from time import sleep

from PyQt5.QtCore import QRunnable

from worker_signals import WorkerSignals


class Timer(QRunnable):
    def __init__(self, fn, *args, **kwargs) -> None:
        super(Timer, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.s = 30
        self.sensor = kwargs['sensor']

    def run(self):
        for t in range(self.s, -1, -1):
            result = {
                't': t,
                'sensor': self.sensor
            }
            self.signals.result.emit(result)
            sleep(1)
