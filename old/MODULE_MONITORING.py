import pandas as pd
import numpy as np
import threading
import pythoncom
import os

######################################## EVENT ########################################
# Custom: Monitoring Time Interval in seconds
TimeInterval = 20

######################################## INPUT PARAMETERS ########################################
# Custom: Number of simulations required
Nr_Of_Simul = 2 # It represent the simulation INPUT PARAMETER of the CONTROL POLICY


######################################## CONTROL PARAMETERS ########################################
# Custom: CONWIP value
ConwipVal = 2  # It is a CONTROL PARAMETER of the CONTROL POLICY
# Custom: Desired KPI
Desired_Throughput = 0.01
Desired_Cycle_Time = 235
Desired_Energy_Consumption = 10

##########################################################################################################
df_origine = pd.read_excel(r"C:\Users\Fedemotta\Desktop\Linea Lab\DB\MESb.xlsx", sheet_name="tblStepDef")
df_proctime = pd.read_excel(r"C:\Users\Fedemotta\Desktop\Linea Lab\DB\PROCTIME.xlsx")
df_orderpos = pd.read_excel(r"C:\Users\Fedemotta\Desktop\Linea Lab\DB\MESb.xlsx", sheet_name="tblOrderPos")
df_tablestep = pd.read_excel(r"C:\Users\Fedemotta\Desktop\Linea Lab\DB\MESb.xlsx", sheet_name="tblStep")
destination_folder = r"C:\Users\Fedemotta\Desktop\Linea Lab\DB\Useful_Tables"
simul_output_file_path1 = r"C:\Users\Fedemotta\Desktop\Linea Lab\Outputs & Extraction\FinishTimes.xlsx" #NB: questo è anche definito nel metodo endsim di plantsimulation
simul_output_file_path2 = r"C:\Users\Fedemotta\Desktop\Linea Lab\Outputs & Extraction\TotEnergyConsumption.xlsx" #NB: questo è anche definito nel metodo endsim di plantsimulation
model_path = r"C:\Users\Fedemotta\Desktop\Linea Lab\LineaPoli_corretta_revLR (3).spp"
##########################################################################################################

######################################## SMART CONTROLLER (Monitoring Application) ########################################
def periodically_monitor(intervallo):
    from DT_Simul import digital_twin_run
    from Monitoring_code import Monitoring
    pythoncom.CoInitialize()
    
    ######################################## DT CALL, INTERFACE ########################################
    DataList = digital_twin_run (Nr_Of_Simul, ConwipVal, df_origine, df_tablestep, df_orderpos, df_proctime, destination_folder, simul_output_file_path1, simul_output_file_path2, model_path)
    
    ######################################## MODULE CALL, CONTROL POLICY ########################################
    Monitoring_Output =  Monitoring (DataList, Desired_Throughput, Desired_Cycle_Time, Desired_Energy_Consumption)
    print(Monitoring_Output)

    ######################################## CONTROL MAP: it takes as trigger event the time interval ########################################
    # It creates a timer that calls the function every 'intervallo' seconds
    t = threading.Timer(intervallo, periodically_monitor, args=[intervallo])
    # CONTROL RULE that triggers the control
    t.start()

# RUN
periodically_monitor(TimeInterval)

