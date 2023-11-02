import pandas as pd
import numpy as np

from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.core.problem import Problem
from pymoo.optimize import minimize
from pymoo.operators.sampling.rnd import PermutationRandomSampling
from pymoo.operators.mutation.inversion import InversionMutation
from pymoo.operators.crossover.ox import OrderCrossover
from pymoo.termination.default import DefaultSingleObjectiveTermination

df_orderpos = pd.read_excel(r"C:\Users\Fedemotta\Desktop\Linea Lab\DB\MESb.xlsx", sheet_name="tblOrderPos")
df_tablestep = pd.read_excel(r"C:\Users\Fedemotta\Desktop\Linea Lab\DB\MESb.xlsx", sheet_name="tblStep")
df_origine = pd.read_excel(r"C:\Users\Fedemotta\Desktop\Linea Lab\DB\MESb.xlsx", sheet_name="tblStepDef")
df_proctime = pd.read_excel(r"C:\Users\Fedemotta\Desktop\Linea Lab\DB\PROCTIME.xlsx")
destination_folder = r"C:\Users\Fedemotta\Desktop\Linea Lab\DB\Useful_Tables"
simul_output_file_path1 = r"C:\Users\Fedemotta\Desktop\Linea Lab\Outputs & Extraction\FinishTimes.xlsx" #NB: questo è anche definito nel metodo endsim di plantsimulation
simul_output_file_path2 = r"C:\Users\Fedemotta\Desktop\Linea Lab\Outputs & Extraction\TotEnergyConsumption.xlsx" #NB: questo è anche definito nel metodo endsim di plantsimulation
model_path = r"C:\Users\Fedemotta\Desktop\Linea Lab\LineaPoli_corretta_revLR (3).spp"

orderpos = df_orderpos

######################################## INPUT PARAMETERS ########################################
# CUSTOM: Nr of simulations
Nr_Of_Simul = 1 #It represent the simulation INPUT PARAMETER of the CONTROL POLICY

######################################## CONTROL PARAMETERS ########################################
ConwipVal = 2 # It is a CONTROL PARAMETER of the CONTROL POLICY

######################################## CONTROL POLICY ########################################
# The following represet the ALGORITHM that should be solved of the CONTROL POLICY
# The following function takes as input the order's position and gives as output the desired objective to be maximized/minimized
def output_computation(orderpos):
    ######################################## DT CALL, INTERFACE ########################################
    from DT_Simul import digital_twin_run
    DataList = digital_twin_run (Nr_Of_Simul, ConwipVal, df_origine, df_tablestep, orderpos, df_proctime, destination_folder, simul_output_file_path1, simul_output_file_path2, model_path)
    df = pd.DataFrame(DataList)
    average_data = df.mean().to_dict()
    ######################################## CONTROL PARAMETER ########################################
    average_TH_value = average_data['average_TH'] # I want to optimize the TH. It represent therefore the CONTROL PARAMETER that was selected by the POLICY
    return (average_TH_value)

def fitness_function(x):
    order = x.astype(int)  # Converti le variabili di decisione in interi
    ordered_df = df_orderpos.iloc[order]  # Permuta l'ordine delle righe
    throughput = output_computation(ordered_df)
    return (-1.0) * throughput  # Massimizzazione del throughput

######################################## SOLVE(INPUT PARAMETERS, CONTROL PARAMETERS) ########################################
# Optimization Algorithm
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
    


# Numero di parti da processare
num_parts = len(df_orderpos) #number of rows of the orderpos dataframe

# Definisci il problema di ottimizzazione
problem = OrderOptimizationProblem(num_parts)

# Definisci l'algoritmo di ottimizzazione
algorithm = GA(
    pop_size=20,
    eliminate_duplicates=True,
    sampling=PermutationRandomSampling(),
    mutation=InversionMutation(),
    crossover=OrderCrossover()
)
termination = DefaultSingleObjectiveTermination(period=50, n_max_gen=10)

# Ottieni la soluzione ottimale
res = minimize(problem,
               algorithm,
               termination,
               seed=1,
               return_values_of=["F"])

# Ottieni l'ordine ottimale delle parti. It is the DECISION VARIABLE THAT IS CREATED
best_order = res.X.astype(int)
ordered_df = df_orderpos.iloc[best_order]
best_throughput = output_computation(ordered_df)




