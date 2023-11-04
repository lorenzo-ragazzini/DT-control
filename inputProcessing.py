import pandas as pd
import numpy as np
import json

def running_orders():
    with open('config.json') as f:
        paths = json.load(f)
        input_path = paths['input_path']
    tblStep_dataframe = pd.read_excel(fr"{input_path}\MESb.xlsx", sheet_name="tblStepDef")
    # Trova l'indice delle righe in cui la colonna "name" non è vuota
    indici_righe_non_vuote = tblStep_dataframe[tblStep_dataframe["End"].notnull()].index
    valori_WPNo = tblStep_dataframe.loc[indici_righe_non_vuote, "WPNo"]
    valori_ONo = tblStep_dataframe.loc[indici_righe_non_vuote, "ONo"]
    valori_OpNo = tblStep_dataframe.loc[indici_righe_non_vuote, "OpNo"]
    # Creazione della matrice
    matrix = np.column_stack((valori_WPNo, valori_ONo, valori_OpNo))
    # Creazione di un DataFrame dalla matrice
    df_matrice = pd.DataFrame(matrix, columns=['WPNo', 'ONo', 'OpNo'])
    # Identificazione dei duplicati basati sulle prime due colonne
    duplicati = df_matrice.duplicated(subset=['WPNo', 'ONo'], keep='last')
    # Selezionare solo le righe uniche
    righe_uniche = df_matrice[~duplicati]
    WPNo_value = righe_uniche['WPNo'].values
    OpNo_value = righe_uniche['OpNo'].values
    # Creazione della matrice
    output = np.column_stack((WPNo_value, OpNo_value))
    df_output = pd.DataFrame(output, columns=['WPNo', 'OpNo'])
    new_column = pd.Series(1, index=df_output.index, name="Number")
    df_output = pd.concat([new_column, df_output], axis=1)
    df_output.to_excel(fr"{input_path}\RunningOrders_Table.xlsx", index=False)
    return(df_output)