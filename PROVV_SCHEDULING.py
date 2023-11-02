import pandas as pd
import numpy as np

from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.core.problem import ElementwiseProblem
from pymoo.optimize import minimize
from pymoo.operators.sampling.rnd import PermutationRandomSampling
from pymoo.operators.mutation.inversion import InversionMutation
from pymoo.operators.crossover.ox import OrderCrossover
from pymoo.termination.default import DefaultSingleObjectiveTermination


# CUSTOM: Nr of simulations
Nr_Of_Simul = 1

df_orderpos = pd.read_excel(r"C:\Users\Fedemotta\Desktop\Linea Lab\DB\MESb.xlsx", sheet_name="tblOrderPos")
df_tablestep = pd.read_excel(r"C:\Users\Fedemotta\Desktop\Linea Lab\DB\MESb.xlsx", sheet_name="tblStep")
df_origine = pd.read_excel(r"C:\Users\Fedemotta\Desktop\Linea Lab\DB\MESb.xlsx", sheet_name="tblStepDef")
df_proctime = pd.read_excel(r"C:\Users\Fedemotta\Desktop\Linea Lab\DB\PROCTIME.xlsx")
destination_folder = r"C:\Users\Fedemotta\Desktop\Linea Lab\DB\Useful_Tables"
simul_output_file_path1 = r"C:\Users\Fedemotta\Desktop\Linea Lab\Outputs & Extraction\FinishTimes.xlsx" #NB: questo è anche definito nel metodo endsim di plantsimulation
simul_output_file_path2 = r"C:\Users\Fedemotta\Desktop\Linea Lab\Outputs & Extraction\TotEnergyConsumption.xlsx" #NB: questo è anche definito nel metodo endsim di plantsimulation
model_path = r"C:\Users\Fedemotta\Desktop\Linea Lab\LineaPoli_corretta_revLR (3).spp"

orderpos = df_orderpos
# The following function takes as input the order's position and gives as output the desired objective to be maximized/minimized
def output_computation(orderpos):
    # DT CALL
    from DT_Simul import digital_twin_run
    DataList = digital_twin_run (Nr_Of_Simul, df_origine, df_tablestep, orderpos, df_proctime, destination_folder, simul_output_file_path1, simul_output_file_path2, model_path)
    df = pd.DataFrame(DataList)
    average_data = df.mean().to_dict()
    average_TH_value = average_data['average_TH'] # I WANT TO OPTIMIZE THE THROUGHPUT. IT SHOULD BE CUSTOMIZED
    return (average_TH_value)

class OrderOptimizationProblem(ElementwiseProblem):

    def __init__(self, num_parts, **kwargs):
        self.num_parts = num_parts

        super(OrderOptimizationProblem, self).__init__(
            n_var=num_parts,
            n_obj=1,
            xl=0,
            xu=num_parts,
            vtype=int,
            **kwargs
        )

    def _evaluate(self, x, out, *args, **kwargs):
        out['F'] = self.objective(x)

    def objective(self, x):
        order = x.astype(int)  # Converti le variabili di decisione in interi
        ordered_df = df_orderpos.iloc[order]  # Permuta l'ordine delle righe
        throughput = output_computation(ordered_df)
        obj = (-1.0) * throughput
        return obj

num_parts = len(df_orderpos) #number of rows of the orderpos dataframe
problem = OrderOptimizationProblem(num_parts)


# Definisci l'algoritmo di ottimizzazione
algorithm = GA(
    pop_size=3, #POPULATION SIZE
    eliminate_duplicates=True,
    sampling=PermutationRandomSampling(),
    mutation=InversionMutation(),
    crossover=OrderCrossover()
)
termination = DefaultSingleObjectiveTermination(period=50, n_max_gen=3)

# Ottieni la soluzione ottimale
res = minimize(problem,
               algorithm,
               termination,
               seed=1,
               verbose=True
               )

# Ottieni l'ordine ottimale delle parti
best_order = res.X.astype(int)
ordered_df = df_orderpos.iloc[best_order]
best_throughput = output_computation(ordered_df)
print(best_throughput)
print(ordered_df)
