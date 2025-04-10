
import PySimpleGUI as sg
import numpy as np
import copy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
from bankers_model import BankersAlgorithm
from test_cases import get_deadlock_case, get_no_deadlock_case
from bankers_gui_layout import BankersGUILayout
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
class BankersAlgorithmGUI:
    def __init__(self):
        self.model = BankersAlgorithm()
        self.layout_manager = BankersGUILayout()
    
    def update_model_from_ui(self, values):
        """Update model data from UI values."""
        try:
            # Get values from UI
            n_processes = self.model.num_processes
            n_resources = self.model.num_resources
            
            # Allocation matrix
            allocation_matrix = np.zeros((n_processes, n_resources), dtype=int)
            for i in range(n_processes):
                for j in range(n_resources):
                    allocation_matrix[i][j] = int(values[self.layout_manager.allocation_inputs[i][j]])
            
            # Max matrix
            max_matrix = np.zeros((n_processes, n_resources), dtype=int)
            for i in range(n_processes):
                for j in range(n_resources):
                    max_matrix[i][j] = int(values[self.layout_manager.max_inputs[i][j]])
            
            # Available resources
            available_resources = np.zeros(n_resources, dtype=int)
            for j in range(n_resources):
                available_resources[j] = int(values[self.layout_manager.available_inputs[j]])
            
            # Update model
            self.model.allocation_matrix = allocation_matrix
            self.model.max_matrix = max_matrix
            self.model.available_resources = available_resources
            
            return True
        
        except ValueError as e:
            sg.popup_error(f"Invalid input: {str(e)}")
            return False
        
    def update_need_display(self, window):
        """Update need matrix display."""
        for i in range(self.model.num_processes):
            for j in range(self.model.num_resources):
                window[self.layout_manager.need_outputs[i][j]].update(str(self.model.need_matrix[i][j]))
    
    def calculate_need(self, window, values):
        """Calculate and display need matrix."""
        if not self.update_model_from_ui(values):
            return
        
        try:
            # Calculate need matrix
            self.model.calculate_need()
            
            # Update need matrix display
            self.update_need_display(window)
            
            # Update results
            window['-RESULTS-'].update("")
            window['-RESULTS-'].print("Need Matrix Calculated!\n")
            window['-RESULTS-'].print("Need Matrix shows how many more resources each process needs.\n")
            window['-RESULTS-'].print("Now you can detect potential deadlocks with the 'Detect Deadlock' button.\n\n")
            window['-RESULTS-'].print("Formula: Need = Max - Allocation\n")
        
        except Exception as e:
            sg.popup_error(f"Failed to calculate need matrix: {str(e)}")