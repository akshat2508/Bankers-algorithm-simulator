# 🏦 Banker's Algorithm Simulator

A comprehensive graphical simulator for the Banker's Algorithm — a classical resource allocation and deadlock avoidance strategy used in operating systems.

---

## 📌 Overview

The Banker's Algorithm Simulator is a Python-based desktop application that allows users to simulate, test, and visualize the working of the Banker's Algorithm. It's built with a focus on educational clarity, interactivity, and real-world relevance.

This tool is ideal for:

- Students trying to understand deadlock avoidance
- Educators creating demonstrations or assignments
- Developers building OS-level resource managers

---

## ✨ Key Features

- **Intuitive GUI** using PySimpleGUI
- **Dynamic Resource Allocation** with step-by-step safety checks
- **Custom Test Case Support** to simulate real-world resource distributions
- **Deadlock Detection & Recovery** simulation logic
- **Graphical Visualizations** of the Wait-For Graph (WFG) and Resource Allocation Graph (RAG)
- **Request Validation** with live feedback on system state

---

## 🧠 Core Concepts Implemented

- **Banker's Algorithm Logic**
- **Safety Sequence Validation**
- **Need Matrix and Available Resource Calculations**
- **Request Handling with Safety Checks**
- **Deadlock Detection through Graph Analysis**

---

## 🗂️ Project Structure

akshat2508-bankers-algorithm-simulator/ ├── README.md → Project documentation ├── main.py → Entry point for the simulator ├── bankers_module.py → Core logic for the Banker's Algorithm ├── bankers_gui_layout.py → UI layout and design (PySimpleGUI) ├── bankers_gui_controller.py → Event handling and logic controller └── test_cases.py → Predefined scenarios for testing

yaml
Copy
Edit

---

## 👥 Developer Roles

**Mansi**  
- Implemented `bankers_module.py` and `test_cases.py`  
- Focused on the algorithm core, safety checks, request processing, and unit testing

**Nandini**  
- Developed `main.py` and `bankers_gui_layout.py`  
- Designed user interface layouts and handled user inputs, forms, and visual components

**Akshat**  
- Built `bankers_gui_controller.py`  
- Connected UI to the algorithm logic, handled events, input validation, and visual result updates

---

## 🛠️ Built With

- **Python 3.6+**
- **PySimpleGUI** - for GUI
- **Matplotlib** - for plotting graphs
- **NetworkX** - for graph-based resource allocation models
- **NumPy** - for matrix operations

---

## ⚙️ Installation

1. Ensure Python 3.6 or above is installed
2. Clone the repository:
   ```bash
   git clone https://github.com/akshat2508/bankers-algorithm-simulator.git
   cd bankers-algorithm-simulator
Install dependencies:

bash
Copy
Edit
pip install pysimplegui matplotlib networkx numpy
🚀 How to Run
Launch the app using:

bash
Copy
Edit
python main.py
Follow on-screen steps to:

Enter number of processes and resources

Define allocation and max requirement matrices

Submit requests and check safety

Visualize WFG and RAG

📊 Example Use Case
Open the app

Load a test case or create a custom input

Click “Check Safety” to see if the current state is safe

Submit a request and validate whether it's grantable

View graphs to understand process dependencies and allocations

🤝 Contributions
We welcome contributions from the community!

Fork the repo

Create a new branch

Make your changes

Submit a Pull Request

📄 License
This project is licensed under the MIT License.

Made with ❤️ by Akshat, Mansi, and Nandini
