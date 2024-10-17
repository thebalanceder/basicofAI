import numpy as np

# Define the function to minimize (example: a simple quadratic function)
def f(x):
    return (x[0] - 1)**2 + (x[1] - 2)**2

# Define the gradient of the function
def grad_f(x):
    return np.array([2*(x[0] - 1), 2*(x[1] - 2)])

# DFP algorithm implementation
def dfp_optimization(f, grad_f, x0, tol=1e-6, max_iter=1000):
    # Initial point and setup
    x_k = np.array(x0)            # Initial guess
    n = len(x_k)
    B_k = np.eye(n)               # Initial Hessian inverse approximation (identity matrix)
    k = 0                         # Iteration counter
    
    # Iterate until convergence or max iterations
    while k < max_iter:
        # Calculate the gradient at the current point
        grad_k = grad_f(x_k)
        
        # Check for convergence (if the norm of the gradient is smaller than tolerance)
        if np.linalg.norm(grad_k) < tol:
            print(f"Converged in {k} iterations.")
            break
        
        # Compute the search direction
        p_k = -B_k @ grad_k
        
        # Perform a simple line search (fixed step size could be used, here we use backtracking line search)
        alpha = line_search(f, x_k, p_k)  # You can replace this with your preferred line search
        
        # Update the current point
        x_new = x_k + alpha * p_k
        
        # Compute the changes in position and gradient
        s_k = x_new - x_k
        y_k = grad_f(x_new) - grad_k
        
        # Update the inverse Hessian matrix using the DFP formula
        term1 = np.outer(s_k, s_k) / np.dot(s_k, y_k)
        term2 = B_k @ np.outer(y_k, y_k) @ B_k / np.dot(y_k, B_k @ y_k)
        B_k = B_k + term1 - term2
        
        # Move to the next iteration
        x_k = x_new
        k += 1
    
    return x_k

# Line search function (Backtracking)
def line_search(f, x_k, p_k, alpha=1, rho=0.8, c=1e-4):
    """
    Backtracking line search: Finds an appropriate step size alpha.
    f : function to minimize
    x_k : current point
    p_k : search direction
    alpha : initial step size (default 1)
    rho : shrinkage factor (0 < rho < 1)
    c : a constant for armijo rule (0 < c < 1)
    """
    while f(x_k + alpha * p_k) > f(x_k) + c * alpha * np.dot(grad_f(x_k), p_k):
        alpha *= rho
    return alpha

# Example usage:
x0 = np.array([0, 0])  # Starting point
optimal_x = dfp_optimization(f, grad_f, x0)
print(f"Optimal point: {optimal_x}")

