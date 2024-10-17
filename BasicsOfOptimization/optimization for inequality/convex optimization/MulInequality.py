import cvxpy as cp

x1=cp.Variable()
x2=cp.Variable()

f1 = x1**2 + x2**2  # Objective 1
f2 = (x1 - 2)**2 + (x2 - 2)**2  # Objective 2

w1=.5
w2=.5

objective=cp.Minimize(w1*f1+w2*f2)
constraints=[]

problem=cp.Problem(objective,constraints)
problem.solve()

print(f"Optimal solution: x1 = {x1.value}, x2 = {x2.value}")
print(f"Optimal value of f1(x1, x2): {f1.value}")
print(f"Optimal value of f2(x1, x2): {f2.value}")
