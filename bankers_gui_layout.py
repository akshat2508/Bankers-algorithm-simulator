
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
        # Max matrix
        max_layout = [[sg.Text(' ', font=header_font)] + [sg.Text(f'R{j}', size=(4, 1), font=header_font) for j in range(num_resources)]]
        for i in range(num_processes):
            row = [sg.Text(f'P{i}', font=font)]
            for j in range(num_resources):
                row.append(sg.Input('0', key=self.max_inputs[i][j], size=(5, 1), font=font, pad=(2, 2)))
            max_layout.append(row)
        
        # Need matrix
        need_layout = [[sg.Text(' ', font=header_font)] + [sg.Text(f'R{j}', size=(4, 1), font=header_font) for j in range(num_resources)]]
        for i in range(num_processes):
            row = [sg.Text(f'P{i}', font=font)]
            for j in range(num_resources):
                row.append(sg.Text('0', key=self.need_outputs[i][j], size=(5, 1), font=font, pad=(2, 2)))
            need_layout.append(row)
        # Available resources
        available_layout = [[sg.Text('Available:', font=font, pad=(5, 5))]]
        resource_row = [sg.Input('0', key=self.available_inputs[j], size=(5, 1), font=font, pad=(3, 3)) for j in range(num_resources)]
        available_layout[0].extend(resource_row)
        
        # Buttons
        button_row = [
            sg.Button('Calculate Need Matrix', key='-CALCULATE_NEED-', font=font, size=(22, 1)),
            sg.Button('Detect Deadlock', key='-DETECT_DEADLOCK-', font=font, size=(18, 1)),
            sg.Button('Recover from Deadlock', key='-RECOVER-', font=font, size=(22, 1)),
            sg.Button('Reset', key='-RESET-', font=font, size=(10, 1))
        ]
        if self.include_rag_button:
            button_row.append(sg.Button('Show WFG', key='-SHOW_RAG-', font=font, size=(14, 1), tooltip='WAIT FOR GRAPH'))

        if self.include_wfg_button:
            button_row.append(sg.Button('Show RAG', key='-SHOW_WFG-', font=font, size=(14, 1), tooltip='R A G'))
        
        # Sample buttons
        sample_row = [
            sg.Button('Load Deadlock Case', key='-DEADLOCK_CASE-', font=font, size=(22, 1)),
            sg.Button('Load No-Deadlock Case', key='-NO_DEADLOCK_CASE-', font=font, size=(22, 1))
        ]
        
        # Frames
        dimensions_frame = sg.Frame('Dimensions', dimensions_frame, font=header_font, pad=(10, 10))
        allocation_frame = sg.Frame('Allocation Matrix', allocation_layout, font=header_font, pad=(10, 10))
        max_frame = sg.Frame('Max Matrix', max_layout, font=header_font, pad=(10, 10))
        need_frame = sg.Frame('Need Matrix', need_layout, font=header_font, pad=(10, 10))
        available_frame = sg.Frame('Available Resources', available_layout, font=header_font, pad=(10, 10))
        
        # Results
        results_frame = [
            [sg.Multiline(size=(100, 20), font=('Courier New', 12), key='-RESULTS-', autoscroll=True, reroute_stdout=True)]
        ]
        
        # Final layout
        layout = [
            [dimensions_frame],
            [sg.HorizontalSeparator(pad=(10, 10))],
            [allocation_frame, max_frame, need_frame],
            [available_frame],
            [sg.HorizontalSeparator(pad=(10, 10))],
            button_row,
            [sg.HorizontalSeparator(pad=(10, 10))],
            sample_row,
            [sg.HorizontalSeparator(pad=(10, 10))],
            [sg.Frame('Results', results_frame, font=header_font, pad=(10, 10))]
        ]
        
        return layout
    