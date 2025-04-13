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
```bash
akshat2508-bankers-algorithm-simulator/ 
├── README.md → Project documentation (you're here)
├── main.py → Entry point for the simulator
├── bankers_module.py → Core logic for the Banker's Algorithm 
├── bankers_gui_layout.py → UI layout and design (PySimpleGUI) 
├── bankers_gui_controller.py → Event handling and logic controller 
└── test_cases.py → Predefined scenarios for testing
```


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

### ✅ Prerequisites
- Python 3.6 or higher installed  
- (Optional) Create a virtual environment for isolation

### 📦 Install Dependencies
```bash
pip install pysimplegui matplotlib networkx numpy
🛠️ Setup
Clone the repository:
git clone https://github.com/akshat2508/bankers-algorithm-simulator.git
cd bankers-algorithm-simulator
```


🚀 Running the Simulator
```bash
Launch the application:
python main.py
```


💡 What You Can Do:
🧮 Enter number of processes and resource types

📊 Input Allocation & Maximum matrices

✅ Run safety checks for current system state

🔄 Submit custom resource requests

📈 Visualize Wait-For Graph (WFG) and Resource Allocation Graph (RAG)



🔍 Example Workflow
```bash
Launch the app using the command above

Use test cases or enter custom values

Click "Check Safety" to verify current system state

Click "Submit Request" to simulate a process asking for more resources

Visualize process/resource states via WFG or RAG buttons
```


🤝 Contributing

# Fork the repository
```bash
git clone <your-fork-url>
cd bankers-algorithm-simulator

# Create a new branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "Add: your feature description"

# Push and open a Pull Request
git push origin feature/your-feature-name
```



👨‍💻 Made with ❤️ by:

Akshat – GUI controller & system integration

Mansi – Core algorithm logic & unit testing

Nandini – User interface design & application flow





