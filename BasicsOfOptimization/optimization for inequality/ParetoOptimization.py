import numpy as np
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.problems import get_problem
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter
from pymoo.core.problem import ElementwiseProblem

class MyProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(n_var=2,n_obj=2,n_constr=0,xl=0,xu=3)

    def _evaluate(self,x,out,*args,**kwargs):
        f1=x[0]**2+x[1]**2
        f2=(x[0]-2)**2+(x[1]-2)**2
        out["F"]=[f1,f2]

problem=MyProblem()
algorithm=NSGA2(pop_size=100)
res=minimize(problem,algorithm,('n_gen',200),seed=1,verbose=False)

pareto_solutions=res.F
pareto_front=res.X

plot=Scatter(title="Pareto Front")
plot.add(pareto_solutions)
plot.show()

print("Pareto-optimal solutions (variables):")
print(pareto_front)
print("Pareto-optimal solutions (objectives):")
print(pareto_solutions)

# If you want the best solution according to one objective (e.g., f1), select the minimum:
best_solution_idx = np.argmin(pareto_solutions[:, 0])  # Minimize f1
best_solution = pareto_front[best_solution_idx]
best_objectives = pareto_solutions[best_solution_idx]

print("\nBest solution based on f1 :")
print("x =", best_solution)
print("f1(x) =", best_objectives[0], "f2(x) =", best_objectives[1])
