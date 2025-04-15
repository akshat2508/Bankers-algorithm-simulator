import numpy as np

def get_deadlock_case():
    """Return sample data that demonstrates a deadlock situation."""
    
    allocation = np.array([
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ])
    
    
    max_matrix = np.array([
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ])
    
    
    available = np.array([0, 0, 0])
    
    return allocation, max_matrix, available

def get_no_deadlock_case():
    """Return sample data that demonstrates a safe state (no deadlock)."""
    
    allocation = np.array([
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ])
    
    
    max_matrix = np.array([
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ])
    
    
    available = np.array([10, 5, 7])
    
    return allocation, max_matrix, available