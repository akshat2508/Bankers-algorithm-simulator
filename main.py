#!/usr/bin/env python3
"""
Banker's Algorithm Simulator
A simulation tool for demonstrating deadlock detection and recovery
using the Banker's Algorithm in operating systems.
"""

from bankers_gui_controller import BankersAlgorithmGUI

def main():
    """Launch the Banker's Algorithm Simulator application"""
    app = BankersAlgorithmGUI()
    app.run()

if __name__ == "__main__":
    main()



