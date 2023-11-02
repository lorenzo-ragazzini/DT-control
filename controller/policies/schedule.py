import pandas as pd
import numpy as np

from operationalController import ControlPolicy

from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.core.problem import Problem
from pymoo.optimize import minimize
from pymoo.operators.sampling.rnd import PermutationRandomSampling
from pymoo.operators.mutation.inversion import InversionMutation
from pymoo.operators.crossover.ox import OrderCrossover
from pymoo.termination.default import DefaultSingleObjectiveTermination

class Schedule(ControlPolicy):
    def run(df_orderpos):
        problem = OrderOptimizationProblem(len(df_orderpos))
        algorithm = GA(pop_size=20,eliminate_duplicates=True,sampling=PermutationRandomSampling(),mutation=InversionMutation(),crossover=OrderCrossover())
        termination = DefaultSingleObjectiveTermination(period=50, n_max_gen=10)
        res = minimize(problem,algorithm,termination,seed=1,return_values_of=["F"])

class OrderOptimizationProblem:
    def __init__(self,num_parts):
        self.num_parts = num_parts
        self.n_var = num_parts
        self.n_obj = 1
        self.xl = np.zeros(num_parts)
        self.xu = np.ones(num_parts)

    def evaluate(self, x, out, *args, **kwargs):
        n_individuals = x.shape[0]
        fitness_values = np.zeros((n_individuals, 1))
        for i in range(n_individuals):
            order = x[i].astype(int)
            ordered_df = df_orderpos.iloc[order]
            throughput = output_computation(ordered_df)
            fitness_values[i, 0] = (-1.0) * throughput
        out["F"] = fitness_values
        return fitness_values 