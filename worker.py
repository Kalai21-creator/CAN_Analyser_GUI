      
from PyQt6.QtCore import QRunnable, pyqtSignal, QObject
import time, random
from helper import data_list

# Signal class
class WorkerSignals(QObject):
    message = pyqtSignal(object)
    error = pyqtSignal(str)

# CAN message structure
class CANMessage:
    def __init__(self, can_id, data, direction="Rx"):
        self.can_id = can_id
        self.data = data
        self.timestamp = time.time()
        self.direction = direction

# CAN worker thread
class CANWorker(QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = WorkerSignals()
        self.running = True
        self.paused = False

    def stop(self):
        self.running = False
        self.paused = False  # Just in case

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def run(self):

        try:
            # while self.running:
            #     if self.paused:
            #         time.sleep(0.1)  # Wait until resumed
            #         continue

            #     # Simulated message
            #     direction = random.choice(["Rx", "Tx"])
            #     can_id = random.choice([0x100, 0x200, 0x300, 0x400, 0x500])
            #     data = [random.randint(0, 255) for _ in range(8)]
            #     msg = CANMessage(can_id, data, direction)

            #     self.signals.message.emit(msg)
            #     time.sleep(0.5)  # Simulate CAN frame rate

            while self.running:
                if self.paused:
                    time.sleep(0.1)
                    continue

                for entry in data_list:
                    if not self.running:  # Check again to allow graceful exit
                        break

                    can_id = entry["canId"]
                    data = entry["Data"]
                    direction = entry["dir"]

                    msg = CANMessage(can_id, data, direction)
                    self.signals.message.emit(msg)
                    
                    time.sleep(0.5)  # Adjust as needed for frame rate

        except Exception as e:
            error_msg = f"Worker encountered an error: {str(e)}"
            print(error_msg)  # Optional: log to console
            self.signals.error.emit(error_msg)
