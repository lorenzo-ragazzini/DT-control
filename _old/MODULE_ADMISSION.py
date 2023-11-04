# Notice that this module does not require the interface with the digital twin, it is just an algorithm

import pandas as pd
import numpy as np
from WPNo_type import OTable


df_orderpos = pd.read_excel(r"C:\Users\Fedemotta\Desktop\Linea Lab\DB\MESb.xlsx", sheet_name="tblOrderPos")
df_tablestep = pd.read_excel(r"C:\Users\Fedemotta\Desktop\Linea Lab\DB\MESb.xlsx", sheet_name="tblStep")
df_origine = pd.read_excel(r"C:\Users\Fedemotta\Desktop\Linea Lab\DB\MESb.xlsx", sheet_name="tblStepDef")
df_proctime = pd.read_excel(r"C:\Users\Fedemotta\Desktop\Linea Lab\DB\PROCTIME.xlsx")
destination_folder = r"C:\Users\Fedemotta\Desktop\Linea Lab\DB\Useful_Tables"
simul_output_file_path1 = r"C:\Users\Fedemotta\Desktop\Linea Lab\Outputs & Extraction\FinishTimes.xlsx" #NB: questo è anche definito nel metodo endsim di plantsimulation
simul_output_file_path2 = r"C:\Users\Fedemotta\Desktop\Linea Lab\Outputs & Extraction\TotEnergyConsumption.xlsx" #NB: questo è anche definito nel metodo endsim di plantsimulation
model_path = r"C:\Users\Fedemotta\Desktop\Linea Lab\LineaPoli_corretta_revLR (3).spp"

# CONTROL POLICY (those are the control parameters)
# CUSTOM: Max Number of parts to be released
Max_rel = 0

# CONTROL POLICY (this is the control algorithm)
def admission (df_orderpos,Max_rel):
    # Get the "Start" column
    start_column = df_orderpos["Start"]
    # Count the number of non-empty cells in the "Start" column
    numberOfReleasedParts = start_column.notna().sum()

    if numberOfReleasedParts > Max_rel:
        # Set all cells in the "ONo" column to empty
        df_orderpos["ONo"] = ""  
        df_orderpos["WPNo"] = ""  
        (df_orders) = OTable(df_orderpos)
        df_orders["Number"] = "" 
    else:
        (df_orders) = OTable(df_orderpos)
      
    return(numberOfReleasedParts, df_orderpos,df_orders)

(numberOfReleasedParts, df_orderpos, df_orders) = admission (df_orderpos,Max_rel)

print(numberOfReleasedParts)
print(df_orders)

# NON SO BENE CHE EVENTO DI TRIGGER UTILIZZARE....