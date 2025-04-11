
import PySimpleGUI as sg
import numpy as np
import copy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
from bankers_module import BankersAlgorithm
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

    def detect_deadlock(self, window, values):
        """Detect deadlock using banker's algorithm."""
        if not self.update_model_from_ui(values):
            return
        
        try:
            # Calculate need matrix first
            self.model.calculate_need()
            self.update_need_display(window)
            
            # Run the detection algorithm
            safe_sequence = self.model.get_safe_sequence()
            
            # Display results
            window['-RESULTS-'].update("")
            
            if safe_sequence:
                window['-RESULTS-'].print("SAFE STATE: No deadlock detected!\n", text_color='green')
                window['-RESULTS-'].print("Safe sequence found: ", end="")
                sequence_str = " → ".join([f"P{i}" for i in safe_sequence])
                window['-RESULTS-'].print(f"{sequence_str}\n\n")
                
                # Show execution details
                window['-RESULTS-'].print("Execution sequence details:\n")
                self.simulate_safe_sequence(window, safe_sequence)
            else:
                window['-RESULTS-'].print("UNSAFE STATE: Potential deadlock detected!\n", text_color='red')
                window['-RESULTS-'].print("No safe execution sequence could be found.\n")
                window['-RESULTS-'].print("Try clicking 'Recover from Deadlock' to see recovery options.\n\n")
                
                # Show processes that could not be executed
                waiting_processes = [i for i in range(self.model.num_processes) 
                                     if i not in self.model.completed_processes]
                window['-RESULTS-'].print("Processes waiting for resources: ", end="")
                waiting_str = ", ".join([f"P{i}" for i in waiting_processes])
                window['-RESULTS-'].print(f"{waiting_str}\n\n")
        
        except Exception as e:
            sg.popup_error(f"Failed to detect deadlock: {str(e)}")
    
    def simulate_safe_sequence(self, window, safe_sequence):
        """Simulate execution of the safe sequence with detailed steps."""
        # Make a copy of model data for simulation
        available = copy.deepcopy(self.model.available_resources)
        allocation = copy.deepcopy(self.model.allocation_matrix)
        
        # Simulate each process execution
        for idx, process_idx in enumerate(safe_sequence):
            # Display current state
            avail_str = ", ".join([f"{r}" for r in available])
            window['-RESULTS-'].print(f"Step {idx+1}: ", text_color='blue', end="")
            window['-RESULTS-'].print(f"Process P{process_idx} executes")
            window['-RESULTS-'].print(f"Available resources before: {avail_str}")
            
            # Execute process (release its resources)
            for j in range(self.model.num_resources):
                available[j] += allocation[process_idx][j]
            
            # Display new available resources
            avail_str = ", ".join([f"{r}" for r in available])
            window['-RESULTS-'].print(f"Process P{process_idx} releases its resources")
            window['-RESULTS-'].print(f"Available resources after: {avail_str}\n")
    
    def recover_deadlock(self, window, values):
        """Suggest deadlock recovery methods."""
        if not self.update_model_from_ui(values):
            return
        
        # Calculate need first
        self.model.calculate_need()
        self.update_need_display(window)
        
        # Get current state
        safe_sequence = self.model.get_safe_sequence()
        
        window['-RESULTS-'].update("")
        
        if safe_sequence:
            window['-RESULTS-'].print("System is in a SAFE state. No recovery needed.\n", text_color='green')
            return
        
        # Show recovery options
        window['-RESULTS-'].print("Deadlock Recovery Options\n", text_color='blue')
        
        # Find process termination suggestions
        window['-RESULTS-'].print("1. Process Termination Method:\n")
        
        # Try terminating processes one by one to find minimum termination set
        terminated_processes = self.find_minimum_termination_set()
        
        if terminated_processes:
            term_str = ", ".join([f"P{i}" for i in terminated_processes])
            window['-RESULTS-'].print(f"Suggestion: Terminate {term_str}")
            window['-RESULTS-'].print("This would release enough resources to resolve the deadlock.\n")
        else:
            window['-RESULTS-'].print("Could not find a suitable termination set.\n")
        
        # Show resource preemption options
        window['-RESULTS-'].print("2. Resource Preemption Method:\n")
        window['-RESULTS-'].print("Consider adding more resources to the system:")
        
        # Find minimum resources needed to resolve deadlock
        needed_resources = self.find_minimum_resource_addition()
        if needed_resources is not None:
            res_str = ", ".join([f"R{i}: {needed_resources[i]}" for i in range(len(needed_resources)) 
                                if needed_resources[i] > 0])
            window['-RESULTS-'].print(f"Add resources: {res_str}")
        else:
            window['-RESULTS-'].print("Could not determine minimum resource addition needed.")
    
    def find_minimum_termination_set(self):
        """Find minimum set of processes to terminate to resolve deadlock."""
        n = self.model.num_processes
        
        # Try terminating single processes first
        for i in range(n):
            temp_model = copy.deepcopy(self.model)
            # Terminate process i (release its resources)
            temp_model.available_resources += temp_model.allocation_matrix[i]
            temp_model.allocation_matrix[i] = np.zeros(temp_model.num_resources)
            temp_model.need_matrix[i] = np.zeros(temp_model.num_resources)
            
            if temp_model.get_safe_sequence():
                return [i]  # Found single process termination solution
        
        # Try pairs of processes
        for i in range(n):
            for j in range(i+1, n):
                temp_model = copy.deepcopy(self.model)
                # Terminate processes i and j
                temp_model.available_resources += temp_model.allocation_matrix[i]
                temp_model.available_resources += temp_model.allocation_matrix[j]
                temp_model.allocation_matrix[i] = np.zeros(temp_model.num_resources)
                temp_model.allocation_matrix[j] = np.zeros(temp_model.num_resources)
                temp_model.need_matrix[i] = np.zeros(temp_model.num_resources)
                temp_model.need_matrix[j] = np.zeros(temp_model.num_resources)
                
                if temp_model.get_safe_sequence():
                    return [i, j]  # Found two-process termination solution
        
        # If no solution with 1 or 2 processes, return None
        return None
    
    def find_minimum_resource_addition(self):
        """Find minimum resources to add to resolve deadlock."""
        # Start with empty additional resources
        additional_resources = np.zeros(self.model.num_resources, dtype=int)
        
        # Keep increasing resources until we find a safe state
        max_iterations = 10  # Prevent infinite loop
        
        for _ in range(max_iterations):
            temp_model = copy.deepcopy(self.model)
            temp_model.available_resources += additional_resources
            
            if temp_model.get_safe_sequence():
                return additional_resources
            
            # Increase the most needed resource
            waiting_processes = [i for i in range(temp_model.num_processes) 
                               if i not in temp_model.completed_processes]
            
            if not waiting_processes:
                break
                
            # Find most-needed resource across waiting processes
            resource_needs = np.zeros(temp_model.num_resources, dtype=int)
            
            for proc in waiting_processes:
                for res in range(temp_model.num_resources):
                    if temp_model.need_matrix[proc][res] > temp_model.available_resources[res]:
                        resource_needs[res] += (temp_model.need_matrix[proc][res] - temp_model.available_resources[res])
            
            if np.sum(resource_needs) == 0:
                break
                
            # Increment the most needed resource
            most_needed = np.argmax(resource_needs)
            additional_resources[most_needed] += 1
        
        return additional_resources if np.sum(additional_resources) > 0 else None
    
    def load_deadlock_case(self, window):
        """Load sample deadlock case."""
        # Get test case data
        allocation, max_matrix, available = get_deadlock_case()
        
        # Set dimensions
        self.model.num_processes = 5
        self.model.num_resources = 3
        
        # Update model and UI
        self.model.allocation_matrix = allocation
        self.model.max_matrix = max_matrix 
        self.model.available_resources = available
        
        # Update UI
        for i in range(self.model.num_processes):
            for j in range(self.model.num_resources):
                window[self.layout_manager.allocation_inputs[i][j]].update(str(allocation[i][j]))
                window[self.layout_manager.max_inputs[i][j]].update(str(max_matrix[i][j]))
        
        for j in range(self.model.num_resources):
            window[self.layout_manager.available_inputs[j]].update(str(available[j]))
        
        # Calculate need and detect deadlock
        self.model.calculate_need()
        self.update_need_display(window)
        
        # Run detection
        values = window.read(timeout=0)[1]  # Get current values
        self.detect_deadlock(window, values)
    
    def load_no_deadlock_case(self, window):
        """Load sample case without deadlock."""
        # Get test case data
        allocation, max_matrix, available = get_no_deadlock_case()
        
        # Set dimensions
        self.model.num_processes = 5
        self.model.num_resources = 3
        
        # Update model and UI
        self.model.allocation_matrix = allocation
        self.model.max_matrix = max_matrix 
        self.model.available_resources = available
        
        # Update UI
        for i in range(self.model.num_processes):
            for j in range(self.model.num_resources):
                window[self.layout_manager.allocation_inputs[i][j]].update(str(allocation[i][j]))
                window[self.layout_manager.max_inputs[i][j]].update(str(max_matrix[i][j]))
        
        for j in range(self.model.num_resources):
            window[self.layout_manager.available_inputs[j]].update(str(available[j]))
        
        # Calculate need and detect deadlock
        self.model.calculate_need()
        self.update_need_display(window)
        
        # Run detection
        values = window.read(timeout=0)[1]  # Get current values
        self.detect_deadlock(window, values)
    
    def reset(self, window):
        """Reset the application state."""
        # Reset model
        self.model.reset()
        
        # Reset UI
        for i in range(self.model.num_processes):
            for j in range(self.model.num_resources):
                window[self.layout_manager.allocation_inputs[i][j]].update('0')
                window[self.layout_manager.max_inputs[i][j]].update('0')
                window[self.layout_manager.need_outputs[i][j]].update('0')
        
        for j in range(self.model.num_resources):
            window[self.layout_manager.available_inputs[j]].update('0')
        
        # Clear results
        window['-RESULTS-'].update("Welcome to Banker's Algorithm Simulator!\n\n"
                                   "1. Start by setting the number of processes and resources.\n"
                                   "2. Create matrices and fill in the allocation and max requirements.\n"
                                   "3. Calculate the Need matrix and detect potential deadlocks.\n\n"
                                   "You can also load sample test cases from the buttons above.\n")
    

