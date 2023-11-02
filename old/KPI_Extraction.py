import pandas as pd
import json
import numpy as np
#from MAIN import ii

# Carica il file Excel
#df = pd.read_excel(r"C:\Users\Fedemotta\Desktop\Linea Lab\Outputs & Extraction\FinishTimes.xlsx")

def Output (Simul_Output_path1,Simul_Output_path2):
    df = pd.read_excel(Simul_Output_path1)
    df2 = pd.read_excel(Simul_Output_path2)
    # Seleziona la colonna dei tempi di uscita
    tempi_uscita = df.iloc[:, 1]

    # Seleziona la quarta colonna (colonna dei cycle time)
    cycle_time = df.iloc[:, 3]

    # Filtra i valori negativi
    cycle_time = cycle_time[cycle_time >= 0]

    # Calcola le differenze tra i tempi di uscita
    differenze_tempi = tempi_uscita.diff()

    # Calcola la media dei tempi di attraversamento del sistema
    media_throughput = 1/differenze_tempi.mean()

    # Calcola la media dei valori del cycle time
    media_cycle_time = cycle_time.mean()

    # Calcola il consumo energetico totale
    tot_energy_consumption = np.sum(df2.iloc[-1,1:].astype(float))

    # Stampa i risultati
    #print("Media del throughput del sistema [parts/s]:", media_throughput)
    #print("Media del cycle time [s]:", media_cycle_time)

    # Visualizzazione del contenuto del JSON
    #print(data)
    return media_throughput, media_cycle_time, tot_energy_consumption

# Creazione del dizionario con i valori
# NON SONO SICURO DEBBA ESSERE FATTO COSI', DA CHIEDERE!!!

def sim_results (average_throughput, average_cycle_time, sim_number, total_energy_consumption):
    data = {
        "simul_Nr": sim_number,  
        "average_TH": average_throughput,
        "average_CT": average_cycle_time,
        "total_energy_consumption": total_energy_consumption
    }

    # Scrivi il dizionario nel file JSON
    with open("output.json", "w") as json_file:
        json.dump(data, json_file)

    # Lettura del file JSON
    with open("output.json", "r") as json_file:
        data = json.load(json_file)
    return data