import PySimpleGUI as sg
import numpy as np
import copy
from bankers_model import BankersAlgorithm
from test_cases import get_deadlock_case, get_no_deadlock_case
from bankers_gui_layout import BankersGUILayout

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