
import PySimpleGUI as sg

sg.theme('LightGreen')
class BankersGUILayout:
    def __init__(self):
        self.allocation_inputs = []
        self.max_inputs = []
        self.need_outputs = []
        self.available_inputs = []
        self.include_rag_button = True  # Set to True by default
        self.include_wfg_button = True
        
    def create_layout(self, num_processes, num_resources):
        """Create the GUI layout with improved sizing."""
        self.setup_input_matrices(num_processes, num_resources)
        font = ('Helvetica', 12)
        header_font = ('Helvetica', 13, 'bold')
        # Input section for dimensions
        dimensions_frame = [
            [sg.Text('Number of Processes:', font=font), sg.Input(num_processes, key='-NUM_PROCESSES-', size=(5, 1), font=font)],
            [sg.Text('Number of Resources:', font=font), sg.Input(num_resources, key='-NUM_RESOURCES-', size=(5, 1), font=font)],
            [sg.Button('Create Matrices', key='-CREATE-', font=font, size=(18, 1))]
        ]

        # Allocation matrix
        allocation_layout = [[sg.Text(' ', font=header_font)] + [sg.Text(f'R{j}', size=(4, 1), font=header_font) for j in range(num_resources)]]
        for i in range(num_processes):
            row = [sg.Text(f'P{i}', font=font)]
            for j in range(num_resources):
                row.append(sg.Input('0', key=self.allocation_inputs[i][j], size=(5, 1), font=font, pad=(2, 2)))
            allocation_layout.append(row)