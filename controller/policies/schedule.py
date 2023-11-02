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
        problem = OrderOptimizationProblem(df_orderpos)
        algorithm = GA(pop_size=20,eliminate_duplicates=True,sampling=PermutationRandomSampling(),mutation=InversionMutation(),crossover=OrderCrossover())
        termination = DefaultSingleObjectiveTermination(period=50, n_max_gen=10)
        res = minimize(problem,algorithm,termination,seed=1,return_values_of=["F"])

class OrderOptimizationProblem:
    def __init__(self,df):
        num_parts = len(df)
        self.n_var = num_parts
        self.n_obj = 1
        self.xl = np.zeros(num_parts)
        self.xu = np.ones(num_parts)
        self.df = df

    def evaluate(self, x, out, *args, **kwargs):
        n_individuals = x.shape[0]
        fitness_values = np.zeros((n_individuals, 1))
        for i in range(n_individuals):
            order = x[i].astype(int)
            ordered_df = self.df.iloc[order]
            throughput = fitness_function(ordered_df)
            fitness_values[i, 0] = (-1.0) * throughput
        out["F"] = fitness_values
        return fitness_values 
    

def fitness_function(orderpos):

    # from DT_Simul import digital_twin_run
    # DataList = digital_twin_run (Nr_Of_Simul, ConwipVal, df_origine, df_tablestep, orderpos, df_proctime, destination_folder, simul_output_file_path1, simul_output_file_path2, model_path)
    
    df = pd.DataFrame(DataList)
    average_data = df.mean().to_dict()
    average_TH_value = average_data['average_TH'] # I want to optimize the TH. It represent therefore the CONTROL PARAMETER that was selected by the POLICY
    return (average_TH_value)