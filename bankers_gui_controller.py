
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
    
    def create_rag_graph(self, values):
        """Create and display a Wait-For Graph visualization."""
        if not self.update_model_from_ui(values):
            return

        # Display loading message
        loading_window = sg.Window("Processing", 
                                [[sg.Text("Generating Wait-For Graph...")]], 
                                modal=True, finalize=True)
        loading_window.refresh()

        # Ensure need matrix is calculated first
        self.model.calculate_need()
        
        # Build the wait-for graph
        G = nx.DiGraph()
        
        # Add process nodes
        for i in range(self.model.num_processes):
            G.add_node(f"P{i}")

        # Check if deadlock detection has been run
        if not hasattr(self.model, "completed_processes"):
            # Run deadlock detection to populate completed_processes
            self.model.get_safe_sequence()
        
        # Identify blocked processes
        blocked_processes = [i for i in range(self.model.num_processes) 
                            if i not in self.model.completed_processes]
        
        # Add edges based on wait-for relationships
        for waiting_process in range(self.model.num_processes):
            # Skip processes that completed in the safety algorithm
            if waiting_process not in blocked_processes:
                continue
                
            # For each resource type
            for resource in range(self.model.num_resources):
                # If this process needs more of this resource than what's available
                if (self.model.need_matrix[waiting_process][resource] > 
                    self.model.available_resources[resource]):
                    
                    # Find processes holding this resource
                    for holding_process in range(self.model.num_processes):
                        # Don't create self-loops
                        if waiting_process == holding_process:
                            continue
                            
                        # If this process holds some of the needed resource
                        if self.model.allocation_matrix[holding_process][resource] > 0:
                            # Add edge: waiting_process → holding_process
                            edge_exists = G.has_edge(f"P{waiting_process}", f"P{holding_process}")
                            if not edge_exists:
                                G.add_edge(f"P{waiting_process}", f"P{holding_process}", 
                                        )
        
        # Detect cycles (cycles indicate deadlocks)
        cycles = list(nx.simple_cycles(G))
        cycle_nodes = set()
        for cycle in cycles:
            cycle_nodes.update(cycle)
        
        # Determine if system is in safe state
        is_safe = len(self.model.completed_processes) == self.model.num_processes

        loading_window.close()

        # Create visualization window
       # Modify the layout and display portion
        graph_layout = [
        [sg.Text("Resource Allocation Wait-For Graph")],
        [sg.Frame('', [[sg.Canvas(key='-CANVAS-', size=(800, 600))]], size=(800, 650), expand_x=True)],
        [sg.Button("Detect Deadlocks"), sg.Button("Save Image"), sg.Button("Close")]
        ]

        graph_window = sg.Window("Wait-For Graph Analysis", graph_layout, finalize=True, 
                     resizable=True, size=(1300, 800))
        


        # Create and configure the visualization
        fig = plt.figure(figsize=(6, 5))
        ax = fig.add_subplot(111)
        
        # Use a simple layout
        pos = nx.spring_layout(G, seed=42)
        
        # Draw nodes with colors indicating their status
        node_colors = []
        for node in G.nodes():
            process_idx = int(node[1:])  # Extract number from "P0", "P1", etc.
            if process_idx in blocked_processes:
                node_colors.append('red')  # Blocked processes
            else:
                node_colors.append('green')  # Safe processes
        
        # Draw nodes
        if G.nodes():
            nx.draw_networkx_nodes(G, pos, node_color=node_colors)
            nx.draw_networkx_labels(G, pos)
        
        # Draw edges
        if G.edges():
            nx.draw_networkx_edges(G, pos, arrows=True)
            
            # Add edge labels showing resource types
            edge_labels = {(u, v): data.get('resource', '') 
                        for u, v, data in G.edges(data=True)}
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
        
        # Highlight cycles if any
        if cycles:
            cycle_edges = []
            for cycle in cycles:
                for i in range(len(cycle)):
                    cycle_edges.append((cycle[i], cycle[(i+1) % len(cycle)]))
            
            nx.draw_networkx_edges(G, pos, edgelist=cycle_edges, 
                                edge_color='blue', width=1.2)
        
        # Add title and remove axes
        if is_safe:
            ax.set_title("Wait-For Graph (System in Safe State)")
        else:
            if cycles:
                ax.set_title("Wait-For Graph (Deadlock Detected)")
            else:
                ax.set_title("Wait-For Graph (Unsafe State, No Direct Deadlock)")
        
        ax.axis('off')
        
        # Add legend
        red_patch = mpatches.Patch(color='red', label='Blocked Process')
        green_patch = mpatches.Patch(color='green', label='Safe Process')
        plt.legend(handles=[red_patch, green_patch], loc='upper right')
        
        # Add explanation
        if G.edges():
            plt.figtext(0.5, 0.01, "An arrow from Pi to Pj means Pi is waiting for resources held by Pj", 
                    ha="center")
        else:
            plt.figtext(0.5, 0.01, "No wait-for relationships detected", 
                    ha="center")
        
        plt.tight_layout()

        # Display graph in the window
        canvas_elem = graph_window['-CANVAS-'].TKCanvas
        figure_canvas_agg = FigureCanvasTkAgg(fig, canvas_elem)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=0)

        # Handle window events
        while True:
            event, values = graph_window.read()
            if event == sg.WIN_CLOSED or event == 'Close':
                break
            elif event == 'Detect Deadlocks':
                if cycles:
                    cycle_info = "Deadlock Cycles Detected:\n\n"
                    for i, cycle in enumerate(cycles):
                        cycle_str = " → ".join(cycle) + " → " + cycle[0]
                        cycle_info += f"Cycle {i+1}: {cycle_str}\n"
                    sg.popup_scrolled(cycle_info, title="Deadlock Analysis", size=(50, 10))
                else:
                    # Show safe sequence if available
                    if is_safe and hasattr(self.model, "safe_sequence"):
                        safe_seq = " → ".join([f"P{p}" for p in self.model.safe_sequence])
                        sg.popup(f"System is in a safe state\n\nSafe sequence: {safe_seq}", 
                                title="Deadlock Analysis")
                    else:
                        sg.popup("No direct deadlock cycles detected, but system may be in UNSAFE state.", 
                                title="Deadlock Analysis")
            elif event == 'Save Image':
                try:
                    filename = sg.popup_get_file('Save graph as', save_as=True, 
                                            file_types=(("PNG Files", "*.png"), ("All Files", "*.*")),
                                            default_extension=".png")
                    if filename:
                        fig.savefig(filename, dpi=300, bbox_inches='tight')
                        sg.popup(f"Graph saved successfully to:\n{filename}")
                except Exception as e:
                    sg.popup_error(f"Error saving file: {str(e)}")

        plt.close(fig)
        graph_window.close()

        

    def create_wfg(self, values):
        """Create and display a Resource Allocation Graph (RAG) visualization."""
        if not self.update_model_from_ui(values):
            return

        # Display loading message
        loading_window = sg.Window("Processing",
                                [[sg.Text("Generating Resource Allocation Graph...")]],
                                modal=True, finalize=True)
        loading_window.refresh()

        # Ensure need matrix is calculated first
        self.model.calculate_need()

        # Build the resource allocation graph
        G = nx.DiGraph()

        # Add process nodes
        for i in range(self.model.num_processes):
            G.add_node(f"P{i}", type='process')

        # Add resource nodes
        for j in range(self.model.num_resources):
            G.add_node(f"R{j}", type='resource')

        # Add assignment edges: Rj → Pi (resource is allocated to a process)
        for i in range(self.model.num_processes):
            for j in range(self.model.num_resources):
                if self.model.allocation_matrix[i][j] > 0:
                    G.add_edge(f"R{j}", f"P{i}")

        # Add request edges: Pi → Rj (process is requesting resource)
        for i in range(self.model.num_processes):
            for j in range(self.model.num_resources):
                if self.model.need_matrix[i][j] > 0 and self.model.available_resources[j] < self.model.need_matrix[i][j]:
                    G.add_edge(f"P{i}", f"R{j}")

        # Detect cycles (optional deadlock detection)
        cycles = list(nx.simple_cycles(G))
        cycle_nodes = set()
        for cycle in cycles:
            cycle_nodes.update(cycle)

        # Determine if system is in safe state
        if not hasattr(self.model, "completed_processes"):
            self.model.get_safe_sequence()
        is_safe = len(self.model.completed_processes) == self.model.num_processes

        loading_window.close()

        # UI layout
        graph_layout = [
            [sg.Text("Resource Allocation Graph")],
            [sg.Frame('', [[sg.Canvas(key='-CANVAS-', size=(800, 600))]], size=(800, 650), expand_x=True)],
            [sg.Button("Detect Deadlocks"), sg.Button("Save Image"), sg.Button("Close")]
        ]

        graph_window = sg.Window("RAG Analysis", graph_layout, finalize=True,
                                resizable=True, size=(1300, 800))

        # Visualization
        fig = plt.figure(figsize=(6, 5))
        ax = fig.add_subplot(111)
        pos = nx.spring_layout(G, seed=42)

        # Node coloring and grouping
        process_nodes = []
        resource_nodes = []
        node_colors = []

        for node in G.nodes():
            ntype = G.nodes[node].get('type')
            if ntype == 'process':
                process_nodes.append(node)
                process_idx = int(node[1:])
                color = 'red' if process_idx not in self.model.completed_processes else 'green'
                node_colors.append(color)
            elif ntype == 'resource':
                resource_nodes.append(node)

        # Draw nodes separately by type
        nx.draw_networkx_nodes(G, pos, nodelist=process_nodes,
                            node_color=['red' if int(n[1:]) not in self.model.completed_processes else 'green' for n in process_nodes],
                            node_shape='o', node_size=400)
        nx.draw_networkx_nodes(G, pos, nodelist=resource_nodes,
                            node_color='skyblue', node_shape='s', node_size=400)

        nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edges(G, pos, arrows=True)

        # Highlight cycles (potential deadlocks)
        if cycles:
            cycle_edges = []
            for cycle in cycles:
                for i in range(len(cycle)):
                    cycle_edges.append((cycle[i], cycle[(i + 1) % len(cycle)]))
            nx.draw_networkx_edges(G, pos, edgelist=cycle_edges,
                                edge_color='blue', width=1.2)

        # Title
        if is_safe:
            ax.set_title("Resource Allocation Graph (System in Safe State)")
        else:
            if cycles:
                ax.set_title("Resource Allocation Graph (Deadlock Detected)")
            else:
                ax.set_title("Resource Allocation Graph (Unsafe State, No Direct Deadlock)")

        ax.axis('off')

        # Legend
        red_patch = mpatches.Patch(color='red', label='Blocked Process')
        green_patch = mpatches.Patch(color='green', label='Safe Process')
        blue_patch = mpatches.Patch(color='skyblue', label='Resource')
        plt.legend(handles=[red_patch, green_patch, blue_patch], loc='upper right')

        # Explanation
        if G.edges():
            plt.figtext(0.5, 0.01, "Arrow from Pi to Rj: Request | Arrow from Rj to Pi: Allocation", ha="center")
        else:
            plt.figtext(0.5, 0.01, "No allocation or request relationships detected", ha="center")

        plt.tight_layout()

        # Display graph in window
        canvas_elem = graph_window['-CANVAS-'].TKCanvas
        figure_canvas_agg = FigureCanvasTkAgg(fig, canvas_elem)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=0)

        # Handle events
        while True:
            event, values = graph_window.read()
            if event == sg.WIN_CLOSED or event == 'Close':
                break
            elif event == 'Detect Deadlocks':
                if cycles:
                    cycle_info = "Deadlock Cycles Detected:\n\n"
                    for i, cycle in enumerate(cycles):
                        cycle_str = " → ".join(cycle) + " → " + cycle[0]
                        cycle_info += f"Cycle {i+1}: {cycle_str}\n"
                    sg.popup_scrolled(cycle_info, title="Deadlock Analysis", size=(50, 10))
                else:
                    if is_safe and hasattr(self.model, "safe_sequence"):
                        safe_seq = " → ".join([f"P{p}" for p in self.model.safe_sequence])
                        sg.popup(f"System is in a safe state\n\nSafe sequence: {safe_seq}",
                                title="Deadlock Analysis")
                    else:
                        sg.popup("No deadlock cycles detected, but system may be in UNSAFE state.",
                                title="Deadlock Analysis")
            elif event == 'Save Image':
                try:
                    filename = sg.popup_get_file('Save graph as', save_as=True,
                                                file_types=(("PNG Files", "*.png"), ("All Files", "*.*")),
                                                default_extension=".png")
                    if filename:
                        fig.savefig(filename, dpi=300, bbox_inches='tight')
                        sg.popup(f"Graph saved successfully to:\n{filename}")
                except Exception as e:
                    sg.popup_error(f"Error saving file: {str(e)}")

        plt.close(fig)
        graph_window.close()









    
    def run(self):
        """Main function to run the application."""
        # Update layout manager to include the RAG button
        self.layout_manager.include_rag_button = True
        
        # Create initial window with default dimensions
        initial_layout = self.layout_manager.create_layout(self.model.num_processes, self.model.num_resources)
        window = sg.Window('Banker\'s Algorithm Simulator', initial_layout, resizable=True, finalize=True)
        
        # Set initial message
        window['-RESULTS-'].print("Welcome to Banker's Algorithm Simulator!\n\n")
        window['-RESULTS-'].print("1. Start by setting the number of processes and resources.\n")
        window['-RESULTS-'].print("2. Create matrices and fill in the allocation and max requirements.\n")
        window['-RESULTS-'].print("3. Calculate the Need matrix and detect potential deadlocks.\n\n")
        window['-RESULTS-'].print("4. You can visualize the Resource Allocation Graph with the 'Show RAG' button.\n\n")
        window['-RESULTS-'].print("You can also load sample test cases from the buttons above.\n")
        
        # Event loop
        while True:
            event, values = window.read()
            
            if event == sg.WIN_CLOSED:
                break
            
            elif event == '-CREATE-':
                # Get new dimensions
                try:
                    n_processes = int(values['-NUM_PROCESSES-'])
                    n_resources = int(values['-NUM_RESOURCES-'])
                    
                    if n_processes < 1 or n_processes > 10 or n_resources < 1 or n_resources > 10:
                        sg.popup_error("Processes and resources must be between 1 and 10")
                        continue
                    
                    # Create new model and UI
                    self.model.num_processes = n_processes
                    self.model.num_resources = n_resources
                    self.model.setup_matrices()
                    
                    # Close current window and create new one
                    window.close()
                    layout = self.layout_manager.create_layout(n_processes, n_resources)
                    window = sg.Window('Banker\'s Algorithm Simulator', layout, resizable=True, finalize=True)
                    
                    # Set initial message
                    window['-RESULTS-'].print("Matrices created successfully!\n\n")
                    window['-RESULTS-'].print("Next steps:\n")
                    window['-RESULTS-'].print("1. Fill in the Allocation Matrix with currently allocated resources\n")
                    window['-RESULTS-'].print("2. Fill in the Max Matrix with maximum resource requirements\n")
                    window['-RESULTS-'].print("3. Fill in Available Resources\n")
                    window['-RESULTS-'].print("4. Click 'Calculate Need Matrix' to continue\n")
                    
                except ValueError:
                    sg.popup_error("Please enter valid numbers")
            
            elif event == '-CALCULATE_NEED-':
                self.calculate_need(window, values)
            
            elif event == '-DETECT_DEADLOCK-':
                self.detect_deadlock(window, values)
            
            elif event == '-RECOVER-':
                self.recover_deadlock(window, values)
            
            elif event == '-RESET-':
                self.reset(window)
            
            elif event == '-DEADLOCK_CASE-':
                self.load_deadlock_case(window)
            
            elif event == '-NO_DEADLOCK_CASE-':
                self.load_no_deadlock_case(window)
                
            elif event == '-SHOW_RAG-':
                self.create_rag_graph(values)
            
            elif event == '-SHOW_WFG-':
                self.create_wfg(values)
        
        window.close()

# Main entry point
if __name__ == "__main__":
    app = BankersAlgorithmGUI()
    app.run()