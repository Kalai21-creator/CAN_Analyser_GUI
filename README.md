

# 🚗 CAN Analyzer GUI

A **Python + PyQt-based CAN Protocol Analyzer GUI** that uses the **PCAN library (PEAK Systems)** to monitor, filter, and export **Controller Area Network (CAN bus)** data in real time.

This tool helps **automotive and embedded engineers** visualize CAN messages, analyze cycle times, and export detailed logs — all through a modern, user-friendly interface.


## 🧩 Features

✅ **Real-time CAN data monitoring** via PCAN interface
✅ Displays **CAN ID, Timestamp, DLC, Data (Hex)**
✅ Calculates **Cycle Time (ms)** and **Message Count**
✅ Identifies **Direction (Tx / Rx)**
✅ **Filter messages** by CAN ID or Data pattern
✅ **Export logs** to CSV with full details
✅ **Start / Stop / Clear** message stream
✅ **Lightweight PyQt GUI** — portable and simple

---

## ⚙️ Tech Stack

| Component     | Technology                   |
| ------------- | ---------------------------- |
| Language      | Python 3.x                   |
| GUI Framework | PyQt5 / PyQt6                |
| CAN Interface | PCANBasic API (PEAK Systems) |
| Data Handling | csv, pandas                  |
| OS Support    | Windows (tested)             |

---

## 🧠 How It Works

1. The GUI connects to a **PEAK PCAN interface** (e.g., `PCAN-USB`, `PCAN-USB FD`).
2. It uses **PCANBasic.dll** to receive CAN frames in real time.
3. Each message is parsed and displayed with fields:

   * **CAN ID**
   * **Timestamp (ms)**
   * **Length (DLC)**
   * **DATA (Hex)**
   * **Cycle Time (ms)** – time gap between consecutive identical IDs
   * **Count** – occurrence count per ID
   * **Direction** – Transmit (Tx) or Receive (Rx)
4. The user can apply **filters** or **export** the displayed table to a CSV file.

---

## 🚀 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Kalai21-creator/can-analyzer-gui.git
cd can-protocol-analyzer-gui
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```
PyQt5
pandas
```

### 3️⃣ Setup PCANBasic Library

* Download and install the **PEAK PCANBasic API**:
  👉 [https://www.peak-system.com/PCAN-Basic.239.0.html](https://www.peak-system.com/PCAN-Basic.239.0.html)
* Ensure the file `PCANBasic.dll` (Windows) or `libpcanbasic.so` (Linux) is accessible (same folder as your script or in system path).

---

### 4️⃣ Run the Application

```bash
python main.py
```

---

## ⚡ Example Usage

* Connect your **PCAN-USB** device.
* Select the desired **baud rate** (e.g., 500 kbps).
* Click **“Connect” → “Start”** to begin monitoring.
* Apply a **filter** (optional).
* Click **“Export”** to save the displayed messages.

---

## 💾 CSV Export Feature

When you click **Export**, the application saves the current CAN log to a `.csv` file with the following columns:

| Column              | Description                                   |
| ------------------- | --------------------------------------------- |
| **CAN ID**          | Identifier of the CAN message                 |
| **Time**            | Timestamp in milliseconds                     |
| **Length**          | Data length code (DLC)                        |
| **DATA (Hex)**      | Data bytes in hexadecimal format              |
| **Cycle Time (ms)** | Time difference between two identical CAN IDs |
| **Count**           | How many times the same CAN ID appeared       |
| **Direction**       | Message direction: Tx / Rx                    |

🗂 Example output:

```csv
CAN ID,Time,Length,DATA (Hex),Cycle Time(ms),Count,Direction
0x123,12:10:05.345,8,11 22 33 44 55 66 77 88,10.5,3,Rx
0x456,12:10:05.355,4,AA BB CC DD,9.8,5,Tx
```

✅ Exported filenames are timestamped, e.g.:

```
can_log_2025-10-28_14-32-11.csv
```

---

## 🔍 Filter Function

* Enter a **CAN ID** (e.g., `0x100`) or **data substring** (e.g., `11 22`) in the filter box.
* Press **Enter** or click **Filter** to view only matching messages.
* To return to all messages, clear the filter input and refresh.

This feature is useful for isolating a specific ECU or signal on a busy CAN bus.

---

## 🧩 GUI Overview

| Section           | Description                                                   |
| ----------------- | ------------------------------------------------------------- |
| **Toolbar**       | Start / Stop / Clear / Export buttons                         |
| **Filter Box**    | Enter ID or data filter                                       |
| **Message Table** | Displays ID, Time, Length, Data, Cycle Time, Count, Direction |
| **Status Bar**    | Connection info and message statistics                        |

---

## 🧠 Future Enhancements

* 📊 Graph view for CAN signal plotting
* 🧩 DBC file decoding support
* 🔁 Multi-channel PCAN support
* 💾 Log replay and playback mode
* 🌙 Dark / Light theme

---

## 🤝 Contributing

Contributions, feedback, and feature requests are welcome!
If you’d like to improve the project:

1. Fork the repo
2. Create your feature branch
3. Submit a Pull Request 🚀

---

## 🧑‍💻 Author

**KALAIVANAN D**


---

## 💬 Repository Description

> A **Python + PyQt CAN Protocol Analyzer GUI** built using the **PCANBasic API**.
> Supports real-time monitoring, filtering, and exporting of CAN bus messages with full metadata — ideal for automotive and embedded development.

---

## 🏷️ Recommended GitHub Tags

```
#Python #PyQt #PCAN #PEAKSystems #CANBus #CANAnalyzer #Automotive #EmbeddedSystems #IoT #GUI
```


