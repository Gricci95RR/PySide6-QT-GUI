from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QMessageBox
import serial
import json

class SerialThread(QThread):
    data_received = Signal(dict)

    def __init__(self):
        super().__init__()
        self.serial = None
        self.running = False

    def run(self):
        try:
            self.serial = serial.Serial('COM12', 921600)
            print("Serial connection status: Open")
            self.running = True
            while self.running:
                if self.serial.in_waiting > 0:
                    line = self.serial.readline().decode('latin-1').strip()
                    print('Debug serial class - data received: ', line)
                    if line.startswith("{") and line.endswith("}"):
                        data = json.loads(line)
                        self.data_received.emit(data)
        except serial.SerialException as e:
            print(f"Serial connection error: {e}")
        finally:
            if self.serial:
                self.serial.close()
                print("Serial connection status: Closed")
    
    def write_to_serial(self, data):
        """
        Method to write a string to the serial line.

        Parameters:
            data (str): The string to write to the serial line.
        """
        if self.serial and self.serial.is_open:
            try:
                self.serial.write(data.encode('latin-1'))
                print("Debug serial class - Data written to serial:", data)
            except Exception as e:
                print("Error writing to serial:", e)
        else:
            print("Serial port is not open.")
            QMessageBox.critical(None, "Serial Port Error", "Serial port is not open.")

    def stop(self):
        self.running = False