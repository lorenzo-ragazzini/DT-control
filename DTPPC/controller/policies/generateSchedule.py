import pandas as pd
import numpy as np
import json

from DTPPC.operationalController import ControlPolicy
from DTPPC.controller.misc import SimulationRequest

from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.core.problem import Problem
from pymoo.optimize import minimize
from pymoo.operators.sampling.rnd import PermutationRandomSampling
from pymoo.operators.mutation.inversion import InversionMutation
from pymoo.operators.crossover.ox import OrderCrossover
from pymoo.termination.default import DefaultSingleObjectiveTermination

class GenerateSchedule(ControlPolicy):
    inputParameters = ['orders']
    def fitness_function(self,sequence,taskResourceInformation,name):
        ctrlUpdate = {"executeSchedule":{"sequence":(sequence+1).tolist()}}
        req = SimulationRequest()
        req['output'] = ['Cmax']
        res = self._controller.dt.interface(name,taskResourceInformation,ctrlUpdate,req)
        return (res['Cmax'])

    class OrderOptimizationProblem(Problem):
        def __init__(self,controlPolicy,taskResourceInformation):
            self.controlPolicy = controlPolicy
            self.taskResourceInformation = taskResourceInformation
            super().__init__(n_var = len(df), n_obj=1, xl=0, xu=1)
        def _evaluate(self, x, out, *args, **kwargs):
            n_individuals = x.shape[0]
            fitness_values = np.zeros((n_individuals, 1))
            for i in range(n_individuals):
                sequence = x[i].astype(int)
                throughput = self.controlPolicy.fitness_function(sequence,self.df)
                # ordered_df = self.df.iloc[order]
                # throughput = self.instance.fitness_function(ordered_df)
                fitness_values[i, 0] = (-1.0) * throughput
            out["F"] = fitness_values
            return fitness_values 
        
    def solve(self,**kwargs):
        taskResourceInformation = kwargs['input']['orders']
        problem = self.OrderOptimizationProblem(self,taskResourceInformation)
        algorithm = GA(pop_size=20,eliminate_duplicates=True,sampling=PermutationRandomSampling(),mutation=InversionMutation(),crossover=OrderCrossover())
        termination = DefaultSingleObjectiveTermination(period=50, n_max_gen=10)
        res = minimize(problem,algorithm,termination,seed=1,return_values_of=["F"])
        return {"sequence":res.X.tolist()}
    
if __name__ == '__main__':
    a=SimulationRequest()
    a[1] = 10
    print(a)
    a
    import pandas as pd
    from digitaltwin import DigitalTwin
    input_path = "C:/Users/Lorenzo/Dropbox (DIG)/Ricerca/GEORGIA TECH/DTbasedcontrol/DB"
    df_orderpos = pd.read_excel(fr"{input_path}\MESb.xlsx", sheet_name="tblOrderPos")
    g=GenerateSchedule()
    class Controller():
        dt=None
    g.controller = Controller()
    dt = DigitalTwin()
    dt.start()
    g.controller.dt = dt
    g.run(df_orderpos)
    '''
    problem = OrderOptimizationProblem(df_orderpos)
    algorithm = GA(pop_size=20,eliminate_duplicates=True,sampling=PermutationRandomSampling(),mutation=InversionMutation(),crossover=OrderCrossover())
    termination = DefaultSingleObjectiveTermination(period=50, n_max_gen=10)
    res = minimize(problem,algorithm,termination,seed=1)
    '''
