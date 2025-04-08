import PySimpleGUI as sg
import numpy as np

class BankersGUILayout:
    def __init__(self):
        self.allocation_inputs = []
        self.max_inputs = []
        self.available_inputs = []
        self.need_outputs = []
        self.font = ('Segoe UI', 11)
        self.header_font = ('Segoe UI', 12, 'bold')
        
        # Set theme
        sg.theme('NeutralBlue')
        
    def create_layout(self, num_processes, num_resources):
        """Create the PySimpleGUI layout based on current dimensions."""
        # Input parameters frame
        params_frame = [
            [sg.Text('Number of Processes:', font=self.font), 
             sg.Spin([i for i in range(1, 11)], initial_value=num_processes, key='-NUM_PROCESSES-', size=(5, 1)),
             sg.Text('Number of Resources:', font=self.font), 
             sg.Spin([i for i in range(1, 11)], initial_value=num_resources, key='-NUM_RESOURCES-', size=(5, 1)),
             sg.Button('Create Matrices', key='-CREATE-', font=self.font)]
        ]
        
        # Test cases row
        test_cases_row = [
            sg.Text('Test Cases:', font=self.font), 
            sg.Button('Load Deadlock Case', key='-DEADLOCK_CASE-', font=self.font),
            sg.Button('Load No Deadlock Case', key='-NO_DEADLOCK_CASE-', font=self.font)
        ]
        
        # Matrix headers
        allocation_header = [[sg.Text('Allocation Matrix', font=self.header_font)]]
        max_header = [[sg.Text('Max Matrix', font=self.header_font)]]
        available_header = [[sg.Text('Available Resources', font=self.header_font)]]
        need_header = [[sg.Text('Need Matrix', font=self.header_font)]]
        
        # Allocation Matrix
        allocation_matrix = [[sg.Text('Process \\ Resource', font=self.font)]]
        for j in range(num_resources):
            allocation_matrix[0].append(sg.Text(f'R{j}', font=self.font))
        
        self.allocation_inputs = []
        for i in range(num_processes):
            row = [sg.Text(f'P{i}', font=self.font)]
            process_row = []
            for j in range(num_resources):
                input_key = f'-ALLOC_{i}_{j}-'
                row.append(sg.Input('0', size=(5, 1), key=input_key, font=self.font))
                process_row.append(input_key)
            allocation_matrix.append(row)
            self.allocation_inputs.append(process_row)
        
        # Max Matrix
        max_matrix = [[sg.Text('Process \\ Resource', font=self.font)]]
        for j in range(num_resources):
            max_matrix[0].append(sg.Text(f'R{j}', font=self.font))
        
        self.max_inputs = []
        for i in range(num_processes):
            row = [sg.Text(f'P{i}', font=self.font)]
            process_row = []
            for j in range(num_resources):
                input_key = f'-MAX_{i}_{j}-'
                row.append(sg.Input('0', size=(5, 1), key=input_key, font=self.font))
                process_row.append(input_key)
            max_matrix.append(row)
            self.max_inputs.append(process_row)
        
        # Available Resources
        available_row = [sg.Text('Available:', font=self.font)]
        self.available_inputs = []
        for j in range(num_resources):
            input_key = f'-AVAIL_{j}-'
            available_row.append(sg.Text(f'R{j}', font=self.font))
            available_row.append(sg.Input('0', size=(5, 1), key=input_key, font=self.font))
            self.available_inputs.append(input_key)
        
        # Need Matrix
        need_matrix = [[sg.Text('Process \\ Resource', font=self.font)]]
        for j in range(num_resources):
            need_matrix[0].append(sg.Text(f'R{j}', font=self.font))
        
        self.need_outputs = []
        for i in range(num_processes):
            row = [sg.Text(f'P{i}', font=self.font)]
            process_row = []
            for j in range(num_resources):
                text_key = f'-NEED_{i}_{j}-'
                row.append(sg.Text('0', size=(5, 1), key=text_key, font=self.font, background_color='white', relief='sunken'))
                process_row.append(text_key)
            need_matrix.append(row)
            self.need_outputs.append(process_row)
        
        # Action buttons
        action_buttons = [
            sg.Button('Calculate Need', key='-CALCULATE_NEED-', font=self.font),
            sg.Button('Detect Deadlock', key='-DETECT_DEADLOCK-', font=self.font),
            sg.Button('Recover from Deadlock', key='-RECOVER-', font=self.font),
            sg.Button('Reset', key='-RESET-', font=self.font)
        ]
        
        # Results area
        results_frame = [
            [sg.Multiline(size=(80, 10), key='-RESULTS-', font=self.font, autoscroll=True)]
        ]
        
        # Layout structure
        layout = [
            [sg.Text('Banker\'s Algorithm Simulator', font=('Segoe UI', 20))],
            [sg.Text('A tool for deadlock detection and recovery in operating systems', font=self.font)],
            [sg.Frame('Input Parameters', params_frame, font=self.header_font)],
            [sg.Frame('Matrices', [
                test_cases_row,
                [sg.Column([
                    [sg.Frame('', allocation_header, border_width=0)],
                    [sg.Frame('', allocation_matrix, border_width=1)],
                    [sg.Frame('', max_header, border_width=0)],
                    [sg.Frame('', max_matrix, border_width=1)]
                ]), 
                sg.Column([
                    [sg.Frame('', available_header, border_width=0)],
                    [sg.Frame('', [available_row], border_width=1)],
                    [sg.Frame('', need_header, border_width=0)],
                    [sg.Frame('', need_matrix, border_width=1)]
                ])]
            ], font=self.header_font)],
            [sg.Frame('Actions', [action_buttons], font=self.header_font)],
            [sg.Frame('Results', results_frame, font=self.header_font)]
        ]
        
        return layout