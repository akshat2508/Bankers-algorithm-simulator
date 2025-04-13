

```markdown
# 🏦 Banker's Algorithm Simulator

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![PySimpleGUI](https://img.shields.io/badge/PySimpleGUI-4.0+-orange.svg)](https://pysimplegui.readthedocs.io/)
[![NetworkX](https://img.shields.io/badge/NetworkX-2.0+-red.svg)](https://networkx.org/)

A comprehensive graphical simulator for the Banker's Algorithm — a classic deadlock avoidance algorithm used in operating systems for resource allocation.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Module Breakdown](#module-breakdown)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

---

## 🔍 Overview

**Banker's Algorithm Simulator** is a Python-based desktop application that allows users to visually simulate the working of the Banker's Algorithm. Ideal for OS students, educators, and curious minds looking to explore safe/unsafe states, deadlocks, and resource allocation.

---

## ✨ Features

- 🔘 **Interactive GUI** — Powered by PySimpleGUI  
- 🔁 **Real-time Simulation** — Step-by-step resource allocation checks  
- 🧠 **Deadlock Detection** — Supports unsafe and deadlock state analysis  
- 📊 **Graph Visualizations** — Wait-For Graph (WFG) & Resource Allocation Graph (RAG)  
- 🧪 **Pre-defined Test Cases** — Test various resource configurations  
- ✍️ **Custom Inputs** — Design your own scenario from scratch  
- 🛡️ **Safety Algorithm Support** — View safe sequences and validation outcomes  

---

## 🗂️ Project Structure

```
akshat2508-bankers-algorithm-simulator/
├── README.md                   # Project documentation
├── main.py                    # Application entry point
├── bankers_gui_layout.py      # GUI layout structure (PySimpleGUI)
├── bankers_gui_controller.py  # Input handling and event logic
├── bankers_module.py          # Core algorithm logic
└── test_cases.py              # Predefined test case inputs
```

---

## 👨‍💻 Module Breakdown

### 🔧 Mansi — `bankers_module.py`, `test_cases.py`

- Implements core Banker's Algorithm logic:
  - Resource allocation
  - Safety checks
  - Deadlock detection
- Test cases include:
  - Safe/unsafe states
  - Edge cases (zero availability, full allocation, etc.)

---

### 🎨 Nandini — `main.py`, `bankers_gui_layout.py`

- GUI structure using **PySimpleGUI**
- Fields for processes, resources, allocation/need matrices
- Interface elements: buttons, tables, input fields, alerts

---

### 🔄 Akshat — `bankers_gui_controller.py`

- Controls user interaction
- Validates input & triggers backend logic
- Manages:
  - Request handling
  - Resetting state
  - Triggering WFG/RAG visualization

---

## 🧰 Technologies Used

### Languages
- Python 3.6+

### Libraries
- [PySimpleGUI](https://pysimplegui.readthedocs.io/) — GUI framework  
- [Matplotlib](https://matplotlib.org/) — Graph plotting  
- [NetworkX](https://networkx.org/) — Graph logic & structure  
- NumPy — Numerical matrix operations  

### Dev Tools
- Git & GitHub for collaboration  
- VSCode for development  

---

## 🚀 Installation

### Prerequisites
Make sure Python 3.6+ is installed.

Install required packages:
```bash
pip install pysimplegui matplotlib networkx numpy
```

### Clone the Repo
```bash
git clone https://github.com/akshat2508/bankers-algorithm-simulator.git
cd bankers-algorithm-simulator
```

---

## 🖥️ Usage

Run the app:
```bash
python main.py
```

### UI Workflow:
- Set the number of processes and resource types
- Input allocation, maximum need, and available resources
- Submit requests and check safety
- Visualize the system's WFG or RAG

---

## 📝 Examples

### ✅ Safety Check
1. Launch the app  
2. Input resource matrices  
3. Click “Check Safety”  
4. View safe sequence or get notified of unsafe state  

### 📌 Custom Requests
1. Select a process  
2. Input resource request  
3. Click “Submit Request”  
4. View if request is safely grantable  

### 🔍 Graph Visualization
- “Show WFG” → Displays Wait-For Graph  
- “Show RAG” → Displays Resource Allocation Graph  

---

## 👥 Contributing

Contributions are welcome!

1. Fork the repository  
2. Create your branch: `git checkout -b feature/your-feature`  
3. Commit your changes: `git commit -m 'Add your message'`  
4. Push and submit a PR  

---

Made with ❤️ by  
**[Akshat](https://github.com/akshat2508)** ·  
**[Mansi]([https://github.com/mansi](https://github.com/mansirathor27))** ·  
**[Nandini]([https://github.com/nandini](https://github.com/Nandinisharma11))**
```

---

Let me know if you want to turn this into a GitHub Pages doc site too, or need help generating a `.exe`/`.app` file with a sexy app icon 👑
