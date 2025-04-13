# 🏦 Banker's Algorithm Simulator

A comprehensive graphical simulator for the **Banker's Algorithm** — a classical resource allocation and deadlock avoidance strategy used in operating systems.

---

## 📌 Overview

The **Banker's Algorithm Simulator** is a desktop application written in Python that enables users to interactively simulate the Banker's Algorithm, observe how processes request and release resources, and visualize how the system reacts to each state change.

Whether you're a student, educator, or operating systems enthusiast, this tool is designed to make learning **deadlock avoidance** engaging and hands-on.

---

## ✨ Key Features

- ✅ **User-Friendly GUI** built with PySimpleGUI
- 🔄 **Dynamic Input Forms** for custom matrix generation
- 🔐 **Live Request Handling** and safety checks
- 📉 **Graphical Visualizations**: Resource Allocation Graph (RAG) and Wait-For Graph (WFG)
- 🔁 **Deadlock Detection & Recovery**
- 📂 **Preloaded Test Cases** and support for custom entries
- 🧪 **Step-by-Step Execution** with clear logs of every decision

---

## 🧠 Core Concepts Implemented

- Banker's Safety Algorithm
- Deadlock Detection Algorithm using Wait-For Graphs
- Resource Allocation Matrix
- Max Requirement Matrix
- Available Resources Calculation
- Need Matrix Derivation
- Request Granting & Rejection with proper logging

---

## 🧮 Mathematical Model Behind

The system validates safety using the following matrices:

- **Available**: Vector of available resources  
- **Max**: Matrix defining max demand of each process  
- **Allocation**: Current resource allocation to each process  
- **Need** = `Max - Allocation`

The simulator performs a safety check after every request:

```text
If Request[i] <= Need[i] and Request[i] <= Available:
    Pretend to allocate → Check if system remains in safe state
    If safe → Grant request
    Else → Deny and revert
🗂️ Project Structure
rust
Copy
Edit
akshat2508-bankers-algorithm-simulator/
├── README.md                  → Project documentation
├── main.py                    → App entry point
├── bankers_module.py          → Core Banker's Algorithm logic
├── bankers_gui_layout.py      → GUI layout (PySimpleGUI)
├── bankers_gui_controller.py  → Logic & input/output controller
└── test_cases.py              → Preset scenarios for quick demos
👥 Developer Contributions
🧩 Mansi
Developed bankers_module.py and test_cases.py

Implemented core algorithm logic, matrix operations, and test validations

🎨 Nandini
Created main.py and bankers_gui_layout.py

Designed user interface, layout flow, and input mechanisms

🔧 Akshat
Handled bankers_gui_controller.py

Built controller for logic-UI integration, event flow, and visual feedback

🛠️ Built With
Python 3.6+

PySimpleGUI – GUI rendering

NumPy – matrix and vector manipulation

NetworkX – graph creation (WFG and RAG)

Matplotlib – rendering graphs

⚙️ Installation
Make sure Python 3.6+ is installed

Clone the repository:

bash
Copy
Edit
git clone https://github.com/akshat2508/bankers-algorithm-simulator.git
cd bankers-algorithm-simulator
Install required packages:

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
Then simply:

Enter the number of processes and resources

Fill the Allocation and Max Requirement matrices

Click “Check Safety” to run the algorithm

Enter custom requests and test outcomes

Visualize current system state through graphs

📊 Example Use Case
Open the app via python main.py

Input 5 processes and 3 resources

Enter allocation and maximum matrices

Click on “Check Safety” to validate current state

Enter a request vector for a process

Instantly see if the request can be granted

Click “Show WFG” or “Show RAG” to understand the system visually

📚 Educational Value
💡 Understand how the system reacts to unsafe states

🔄 Experiment with different matrices and scenarios

📈 See how deadlock conditions arise and how the algorithm avoids them

🧠 Great for demos, assignments, lab work, and viva prep


🤝 Contributions
We love contributors! To contribute:

Fork the repository

Create a feature branch

Make your changes

Submit a Pull Request

New features, bug fixes, and documentation improvements are always welcome ✨

📄 License
This project is licensed under the MIT License.
Feel free to use, modify, and distribute with attribution.

🔚 Final Notes
This simulator was created to bridge the gap between textbook theory and practical understanding of deadlock avoidance in operating systems. With visual feedback, simplified input, and thorough implementation, it’s designed to be both technically solid and fun to use!

Made with ❤️ by Akshat, Mansi, and Nandini
