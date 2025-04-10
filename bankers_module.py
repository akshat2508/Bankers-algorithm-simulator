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
    
    def is_request_granted(self, process_idx):
        """Check if the process's resource request can be granted."""
        for j in range(self.num_resources):
            if self.need_matrix[process_idx][j] > self.available_resources[j]:
                return False
        return True
    
    def get_safe_sequence(self):
        """Run banker's algorithm to find a safe sequence."""
        
        work = copy.deepcopy(self.available_resources)
        finish = [False] * self.num_processes
        safe_sequence = []
        self.completed_processes = []
        
        
        while len(safe_sequence) < self.num_processes:
            found = False
            
            
            for i in range(self.num_processes):
                if not finish[i]:
                    
                    can_allocate = True
                    for j in range(self.num_resources):
                        if self.need_matrix[i][j] > work[j]:
                            can_allocate = False
                            break
                    
                    if can_allocate:
                        
                        safe_sequence.append(i)
                        self.completed_processes.append(i)
                        finish[i] = True
                        found = True
                        
                       
                        for j in range(self.num_resources):
                            work[j] += self.allocation_matrix[i][j]
                        
                        break
            
            if not found:
                break
        
        
        if len(safe_sequence) == self.num_processes:
            return safe_sequence
        else:
            return None