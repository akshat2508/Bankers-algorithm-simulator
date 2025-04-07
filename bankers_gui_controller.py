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