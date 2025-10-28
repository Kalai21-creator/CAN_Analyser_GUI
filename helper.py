
# helper.py

from PyQt6.QtWidgets import QTableWidget, QMessageBox

def filter_table_data(table: QTableWidget, keyword: str):
    for row in range(table.rowCount()):
        match = False
        for col in [0, 3]:  # Filter by CAN ID and Data
            item = table.item(row, col)
            if item and keyword in item.text().lower():
                match = True
                break
        table.setRowHidden(row, not match)
  
data_list = [
    {
        "canId": 0x18FECA00,
        "Data": [0x88, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
        "dir": "Tx"
    },
    {
        "canId": 0x18FECA00,
        "Data": [0x08, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
        "dir": "Rx"
    },
    {
        "canId": 0x18FDC600,
        "Data": [0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
        "dir": "Tx"
    },
    {
        "canId": 0x18FEEE00,
        "Data": [0x98, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
        "dir": "Tx"
    },
    {
        "canId": 0x18FEEF00,
        "Data": [0xFF, 0xFF, 0xFF, 0x00, 0xFF, 0xFF, 0xFF, 0xFF],
        "dir": "Tx"
    },
    {
        "canId": 0x18FECA00,
        "Data": [0x80, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
        "dir": "Rx"
    },
    {
        "canId": 0x18FEFF00,
        "Data": [0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
        "dir": "Rx"
    }
]
