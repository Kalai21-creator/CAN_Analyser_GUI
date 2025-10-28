'''
import time,csv
from worker import *
from PyQt6.QtGui import QColor

from PyQt6.QtWidgets import (

    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox ,
    QSplitter, QLabel, QSizePolicy, QFrame, QFileDialog,QLineEdit
)

from worker import CANWorker
from PyQt6.QtCore import Qt, QThreadPool
from datetime import datetime

from helper import filter_table_data

#main appscreen window/mainwindow
class CANAnalyzerGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CAN Analyser GUI")
        self.setFixedSize(1920, 1080)
        self.threadpool = QThreadPool()
        self.worker = None

        self.last_times = {}
        self.counts = {}
        self.all_messages = []

        self.setup_ui()


    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(10,10,10,10)
        main_layout.setSpacing(10)


        #control buttons widgets
      # Control buttons layout at top-left
        control_layout = QHBoxLayout()

        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Filter by ID or DATA...")
        #self.filter_input.setFixedWidth(25000)
        self.filter_input.setMinimumWidth(150)


        filter_label = QLabel("Filter:")
        filter_label.setStyleSheet("font-weight: bold;")

        self.start_btn = QPushButton("Start 🟢")
        self.stop_btn = QPushButton("Pause ⏹")
        self.resume_btn = QPushButton("Resume ▶️")
        self.csv_btn = QPushButton("CSV 📊")

        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.stop_btn)
        control_layout.addWidget(self.resume_btn)
        control_layout.addWidget(self.csv_btn)
        control_layout.addWidget(filter_label)
        control_layout.addWidget(self.filter_input)
        control_layout.addStretch()
        main_layout.addLayout(control_layout)


        #add color to button
        self.start_btn.setStyleSheet("background-color: #80ffaa; font-weight: bold;")
        self.stop_btn.setStyleSheet("background-color:  #ffb3d9; font-weight: bold;")
        self.resume_btn.setStyleSheet("background-color: #ccccff; font-weight: bold;")
        self.csv_btn.setStyleSheet("background-color: #ff6699; font-weight: bold;")
        self.filter_input.setStyleSheet("background-color: #ffdead; font-weight: bold;")

        
        #Split Horizontally for RX and TX
        h_splitter = QSplitter(Qt.Orientation.Horizontal)
        #left side with vertical labels
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.rx_label = self.vertical_label("RECEIVE")
        self.tx_label = self.vertical_label("TRANSMIT")
        left_layout.addWidget(self.rx_label)
        left_layout.addSpacing(40)
        left_layout.addWidget(self.tx_label)
        h_splitter.addWidget(left_widget)

        #Right pane with two tables
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        self.rx_table = self.create_table()
        self.tx_table = self.create_table()
        v_splitter = QSplitter(Qt.Orientation.Vertical)
        v_splitter.addWidget(self.rx_table)
        v_splitter.addWidget(self.tx_table)
        v_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color:  #ffffff;  /* dark gap between RX and TX */
                height: 6px;
            }
        """)

        right_layout.addWidget(v_splitter)

        h_splitter.addWidget(right_widget)
        h_splitter.setStretchFactor(0, 1)
        h_splitter.setStretchFactor(1, 6)

        main_layout.addWidget(h_splitter)
        
        #connect buttons
        self.start_btn.clicked.connect(self.start_worker)
        self.stop_btn.clicked.connect(self.pause_worker)
        self.resume_btn.clicked.connect(self.resume_worker)
        self.csv_btn.clicked.connect( self.export_csv)
        self.filter_input.textChanged.connect(self.apply_filter)

    #to start the worker thread
    def start_worker(self):
        if self.worker is None:
            self.worker = CANWorker()
            self.worker.signals.message.connect( self.handle_message)
            self.threadpool.start(self.worker)

   #to pause the worker thread 
    def pause_worker(self):
        if self.worker:
            self.worker.pause()

    #to resume the worker thread
    def resume_worker(self):
        if self.worker:
            self.worker.resume()

    #to display the Transmit/recive in Veritcal way
    def vertical_label(self, text):
        label = QLabel("\n".join(text))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font: bold 14pt;")
        label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        return label
    
    #to create a table with heading
    def create_table(self):
        table = QTableWidget(0, 6)
        table.setHorizontalHeaderLabels([
            "CAN ID", "Time", "Length", "DATA (Hex)", "Cycle Time(ms)", "Count"
        ])

        table.verticalHeader().setVisible(False)

        table.setStyleSheet("""
            QTableWidget {
                font-size: 12pt;
                border: 2px solid #333; /* Outer border of the table */
                gridline-color: #333;   /* Color of internal grid lines */
            }

            QHeaderView::section {
                font-weight: bold;
                font-size: 13pt;
                background-color: #7575a3;
                color: white;
                padding: 4px;
                border: 1px solid #222;
            }

            QTableWidget::item {
                border: 1px solid #333;  /* Each cell border */
                padding: 4px;
            }
        """)

        table.setColumnWidth(0, 250)
        table.setColumnWidth(1, 250)
        table.setColumnWidth(2, 250)
        table.setColumnWidth(3, 500)
        table.setColumnWidth(4, 250)
        table.setColumnWidth(5, 250)

        return table
    


    def apply_filter(self):
        keyword = self.filter_input.text().strip().lower()
        filter_table_data(self.rx_table, keyword)
        filter_table_data(self.tx_table, keyword)

    
    # def handle_message(self, msg):
    #     table = self.rx_table if msg.direction == "Rx" else self.tx_table
    #     can_id = msg.can_id
    #     data = msg.data
    #     length = len(data)
    #     hex_data = " ".join(f'{b:02X}' for b in data)
    #     now = time.time()
    #     last_time = self.last_times.get(can_id, now)
    #     cycle_time = int((now - last_time) * 1000)
    #     self.last_times[can_id] = now
    #     self.counts[can_id] = self.counts.get(can_id, 0) + 1
    #     count = self.counts[can_id]
    #     self.all_messages.append(msg)
    #     #Time HH:MM:SS format
    #     dt = datetime.fromtimestamp(now)
    #     formatted_time = dt.strftime("%H:%M:%S")


    #     row = table.rowCount()
    #     table.insertRow(row)
    #     table.setItem(row, 0, QTableWidgetItem(f"0x{can_id:X}"))
    #     table.setItem(row, 1, QTableWidgetItem(formatted_time))
    #     table.setItem(row , 2, QTableWidgetItem(str(length)))
    #     table.setItem(row, 3, QTableWidgetItem(hex_data))
    #     table.setItem(row, 4 , QTableWidgetItem(str(cycle_time)))
    #     table.setItem(row, 5, QTableWidgetItem(str(count)))
    #     table.scrollToBottom()


    #to display all messgae into the table
    def handle_message(self, msg):
        table = self.rx_table if msg.direction == "Rx" else self.tx_table
        can_id = msg.can_id
        data = msg.data
        length = len(data)
        hex_data = " ".join(f'{b:02X}' for b in data)

        now = msg.timestamp  #  more accurate than time.time()
        can_id_hex = f"0x{can_id:X}"

        last_time = self.last_times.get(can_id_hex, now)
        cycle_time = int((now - last_time) * 1000)
        self.last_times[can_id_hex] = now

        count = self.counts.get(can_id_hex, 0) + 1
        self.counts[can_id_hex] = count

        #  Attach to message before saving
        msg.cycle_time = cycle_time
        msg.count = count

        #  Store message for export
        self.all_messages.append(msg)

        # GUI update
        dt = datetime.fromtimestamp(now)
        formatted_time = dt.strftime("%H:%M:%S")

        row = table.rowCount()
        table.insertRow(row)
        table.setItem(row, 0, QTableWidgetItem(can_id_hex))
        table.setItem(row, 1, QTableWidgetItem(formatted_time))
        table.setItem(row, 2, QTableWidgetItem(str(length)))
        table.setItem(row, 3, QTableWidgetItem(hex_data))
        table.setItem(row, 4, QTableWidgetItem(str(cycle_time)))
        table.setItem(row, 5, QTableWidgetItem(str(count)))
        table.scrollToBottom()


    #to close the app
    def closeEvent(self, event):
        if self.worker:
            self.worker.stop()
        event.accept()

    def export_csv(self):
     if not self.all_messages:
         QMessageBox.information(self, "Export CSV","No messages to export.")
         return False
     
     path, _ = QFileDialog.getSaveFileName(
         self, "Save CSV", "", "CSV files (*.csv);;All Files(*)"
     )

     if not path:
         return False
     
     try:
        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["CAN ID", "Time", "Length", "DATA (Hex)", "Cycle Time(ms)", "Count", "Direction"])

            for msg in self.all_messages:
                t = datetime.fromtimestamp(msg.timestamp)
                time_str = t.strftime("%H:%M:%S")

                can_id = f"0x{msg.can_id:X}"
                length = len(msg.data)
                data_hex = ' '.join(f"{b:02X}" for b in msg.data)

                #  Use already-stored values
                cycle_time = msg.cycle_time if hasattr(msg, 'cycle_time') else ""
                count = msg.count if hasattr(msg, 'count') else ""

                writer.writerow([can_id, time_str, length, data_hex, cycle_time, count, msg.direction])
    
        QMessageBox.information(self, "Export CSV", f"Exported {len(self.all_messages)} messages to:\n{path}")
     except Exception as e:
            QMessageBox.critical(self, "Export CSV", f"Failed to export CSV:\n{str(e)}")
    
            
            '''


import time, csv
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
    QSplitter, QLabel, QSizePolicy, QFileDialog, QLineEdit
)
from PyQt6.QtCore import Qt, QThreadPool
from datetime import datetime

from worker import CANWorker
from helper import filter_table_data


class CANAnalyzerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CAN Analyser GUI")
        self.setFixedSize(1920, 1080)
        self.threadpool = QThreadPool()
        self.worker = None

        self.last_times = {}
        self.counts = {}
        self.all_messages = []

        self.setup_ui()


    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Control buttons
        control_layout = QHBoxLayout()

        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Filter by ID or DATA...")
        self.filter_input.setMaximumWidth(250)

        filter_label = QLabel("Filter:")
        filter_label.setStyleSheet("font-weight: bold;")

        self.start_btn = QPushButton("Start 🟢")
        self.stop_btn = QPushButton("Pause ⏹")
        self.resume_btn = QPushButton("Resume ▶️")
        self.csv_btn = QPushButton("CSV 📊")

        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.stop_btn)
        control_layout.addWidget(self.resume_btn)
        control_layout.addWidget(self.csv_btn)
        control_layout.addWidget(filter_label)
        control_layout.addWidget(self.filter_input)
        control_layout.addStretch()
        main_layout.addLayout(control_layout)

        # Button styles
        self.start_btn.setStyleSheet("background-color: #80ffaa; font-weight: bold;")
        self.stop_btn.setStyleSheet("background-color:  #ffb3d9; font-weight: bold;")
        self.resume_btn.setStyleSheet("background-color: #ccccff; font-weight: bold;")
        self.csv_btn.setStyleSheet("background-color: #ff6699; font-weight: bold;")
        self.filter_input.setStyleSheet("background-color: #ffdead; font-weight: bold;")

        # Horizontal Splitter
        h_splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left side labels
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.rx_label = self.vertical_label("RECEIVE")
        self.tx_label = self.vertical_label("TRANSMIT")
        left_layout.addWidget(self.rx_label)
        left_layout.addSpacing(40)
        left_layout.addWidget(self.tx_label)
        h_splitter.addWidget(left_widget)

        # Right side tables
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        self.rx_table = self.create_table()
        self.tx_table = self.create_table()
        v_splitter = QSplitter(Qt.Orientation.Vertical)
        v_splitter.addWidget(self.rx_table)
        v_splitter.addWidget(self.tx_table)

        v_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color:  #ffffff;
                height: 6px;
            }
        """)

        right_layout.addWidget(v_splitter)
        h_splitter.addWidget(right_widget)
        h_splitter.setStretchFactor(0, 1)
        h_splitter.setStretchFactor(1, 6)
        main_layout.addWidget(h_splitter)

        # Connect buttons
        self.start_btn.clicked.connect(self.start_worker)
        self.stop_btn.clicked.connect(self.pause_worker)
        self.resume_btn.clicked.connect(self.resume_worker)
        self.csv_btn.clicked.connect(self.export_csv)
        self.filter_input.textChanged.connect(self.apply_filter)



    def vertical_label(self, text):
        label = QLabel("\n".join(text))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font: bold 14pt;")
        label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        return label


    def create_table(self):
        table = QTableWidget(0, 6)
        table.setHorizontalHeaderLabels([
            "CAN ID", "Time", "Length", "DATA (Hex)", "Cycle Time(ms)", "Count"
        ])
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        table.setStyleSheet("""
            QTableWidget {
                font-size: 12pt;
                border: 2px solid #333;
                gridline-color: #333;
            }
            QHeaderView::section {
                font-weight: bold;
                font-size: 13pt;
                background-color: #7575a3;
                color: white;
                padding: 4px;
                border: 1px solid #222;
            }
            QTableWidget::item {
                font-weight: bold;
                border: 1px solid #333;
                padding: 4px;
            }
        """)

        table.setColumnWidth(0, 250)
        table.setColumnWidth(1, 250)
        table.setColumnWidth(2, 250)
        table.setColumnWidth(3, 500)
        table.setColumnWidth(4, 250)
        table.setColumnWidth(5, 250)

        return table


    def start_worker(self):
        if self.worker is None:
            self.worker = CANWorker()
            self.worker.signals.message.connect(self.handle_message)
            self.threadpool.start(self.worker)


    def pause_worker(self):
        if self.worker:
            self.worker.pause()


    def resume_worker(self):
        if self.worker:
            self.worker.resume()


    def apply_filter(self):
        keyword = self.filter_input.text().strip().lower()
        filter_table_data(self.rx_table, keyword)
        filter_table_data(self.tx_table, keyword)


    def handle_message(self, msg):
        table = self.rx_table if msg.direction == "Rx" else self.tx_table
        can_id = msg.can_id
        data = msg.data
        length = len(data)
        hex_data = " ".join(f'{b:02X}' for b in data)

        now = msg.timestamp
        can_id_hex = f"0x{can_id:X}"

        last_time = self.last_times.get(can_id_hex, now)
        cycle_time = int((now - last_time) * 1000)
        self.last_times[can_id_hex] = now

        count = self.counts.get(can_id_hex, 0) + 1
        self.counts[can_id_hex] = count

        msg.cycle_time = cycle_time
        msg.count = count

        self.all_messages.append(msg)

        dt = datetime.fromtimestamp(now)
        formatted_time = dt.strftime("%H:%M:%S")

        row = table.rowCount()
        table.insertRow(row)

        values = [
            can_id_hex,          # CAN ID
            formatted_time,      # Time
            str(length),         # Length
            hex_data,            # DATA
            str(cycle_time),     # Cycle Time
            str(count)           # Counts
        ]

        for col, value in enumerate(values):
            item = QTableWidgetItem(value)
            item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            table.setItem(row, col, item)

        table.scrollToBottom()


    def export_csv(self):
        if not self.all_messages:
            QMessageBox.information(self, "Export CSV", "No messages to export.")
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Save CSV", "", "CSV files (*.csv);;All Files(*)"
        )

        if not path:
            return

        try:
            with open(path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["CAN ID", "Time", "Length", "DATA (Hex)", "Cycle Time(ms)", "Count", "Direction"])

                for msg in self.all_messages:
                    t = datetime.fromtimestamp(msg.timestamp)
                    time_str = t.strftime("%H:%M:%S")
                    can_id = f"0x{msg.can_id:X}"
                    length = len(msg.data)
                    data_hex = ' '.join(f"{b:02X}" for b in msg.data)
                    cycle_time = msg.cycle_time if hasattr(msg, 'cycle_time') else ""
                    count = msg.count if hasattr(msg, 'count') else ""

                    writer.writerow([can_id, time_str, length, data_hex, cycle_time, count, msg.direction])

            QMessageBox.information(self, "Export CSV", f"Exported {len(self.all_messages)} messages to:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export CSV", f"Failed to export CSV:\n{str(e)}")


    def closeEvent(self, event):
        if self.worker:
            self.worker.stop()
        event.accept()
