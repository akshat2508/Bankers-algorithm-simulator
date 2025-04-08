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
    def setup_matrices(self):
        """Initialize matrices with zeros."""
        self.allocation_matrix = np.zeros((self.num_processes, self.num_resources), dtype=int)
        self.max_matrix = np.zeros((self.num_processes, self.num_resources), dtype=int)
        self.need_matrix = np.zeros((self.num_processes, self.num_resources), dtype=int)
        self.available_resources = np.zeros(self.num_resources, dtype=int)
        self.completed_processes = []
    
    def calculate_need(self):
        """Calculate the need matrix from max and allocation."""
        self.need_matrix = self.max_matrix - self.allocation_matrix
        
        
        if np.any(self.need_matrix < 0):
            raise ValueError("Invalid allocation: Some allocations exceed maximum claims")