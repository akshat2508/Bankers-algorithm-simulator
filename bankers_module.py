import numpy as np
import copy

class BankersAlgorithm:
    """Model class implementing Banker's Algorithm."""
    
    def __init__(self, num_processes=5, num_resources=3):
        """Initialize the model with default dimensions."""
        self.num_processes = num_processes
        self.num_resources = num_resources
        self.reset()
    
    def reset(self):
        """Reset the model state."""
        self.setup_matrices()
        self.completed_processes = []