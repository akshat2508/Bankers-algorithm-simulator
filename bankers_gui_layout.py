
import PySimpleGUI as sg

sg.theme('LightGreen')
class BankersGUILayout:
    def __init__(self):
        self.allocation_inputs = []
        self.max_inputs = []
        self.need_outputs = []
        self.available_inputs = []
        self.include_rag_button = True  # Set to True by default
        
    def create_layout(self, num_processes, num_resources):
        """Create the GUI layout with improved sizing."""
        self.setup_input_matrices(num_processes, num_resources)
        font = ('Helvetica', 12)
        header_font = ('Helvetica', 13, 'bold')