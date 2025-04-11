import numpy as np

def get_deadlock_case():
    """Return sample data that demonstrates a deadlock situation."""
    # Set allocation matrix
    allocation = np.array([
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ])
    
    # Set max matrix
    max_matrix = np.array([
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ])
    
    # Set available resources to create deadlock
    available = np.array([0, 0, 0])
    
    return allocation, max_matrix, available