import pandas as pd
import numpy as np
import json

def WPNo_Orders():
    with open('config.json') as f:
        paths = json.load(f)
        input_path = paths['input_path']
    df_origine = pd.read_excel(fr"{input_path}\MESb.xlsx", sheet_name="tblStepDef")
    df_proctime = pd.read_excel(fr"{input_path}\PROCTIME.xlsx")
    df_orderpos = pd.read_excel(fr"{input_path}\MESb.xlsx", sheet_name="tblOrderPos")

    # Estrai i valori dalla prima colonna chiamata "WPNo"
    wpno_values = df_origine["WPNo"].drop_duplicates().tolist()
    for value in wpno_values:
        # Filtra le righe corrispondenti al valore corrente
        df_filtrato = df_origine[df_origine["WPNo"] == value][["Description", "OpNo"]]
        # Unisci la tabella filtrata con la colonna "Mean" corrispondente dalla tabella "PROCTIME"
        df_unione = pd.merge(df_filtrato, df_proctime[df_proctime["OpNo"].isin(df_filtrato["OpNo"])][["OpNo", "Mean"]],on="OpNo", how="left")   
        # Rinomina la colonna "Mean" in "ProcTime"
        df_unione.rename(columns={"Mean": "ProcTime"}, inplace=True)
        #  Crea un nuovo dataframe con le colonne filtrate
        df_salvataggio = pd.DataFrame(df_unione)
        # Salva il dataframe in un nuovo file Excel
        nome_file_salvataggio = fr"{input_path}\WPNo_OpNo_ProcTime_{value}.xlsx"
        df_salvataggio.to_excel(nome_file_salvataggio, index=False)
    print(f"WPNo_OpNo_ProcTime tables have been created")
    
    # Estrazione della colonna WPNo
    df_orders = df_orderpos["WPNo"]
    # Crea una nuova colonna con valori costanti di 1
    new_column = pd.Series(1, index=df_orders.index, name="Number")
    # Aggiungi la nuova colonna al DataFrame
    df_orders = pd.concat([new_column, df_orders], axis=1)
    # Esportare la tabella in un file Excel
    df_orders.to_excel(fr"{input_path}\Order_Table.xlsx", index=False)
    print(f"Order_Table has been created")
    return (df_orders)


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
    #print(matrix)

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
    # return(df_output)
