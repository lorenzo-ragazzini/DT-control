import pandas as pd
import numpy as np
import json

def planned_orders(simple=False):
    with open('config.json') as f:
        paths = json.load(f)
        input_path = paths['input_path']
    df_orderpos = pd.read_excel(fr"{input_path}\MESb.xlsx", sheet_name="tblOrderPos")
    if not simple:
        df_origine = pd.read_excel(fr"{input_path}\MESb.xlsx", sheet_name="tblStepDef")
        df_proctime = pd.read_excel(fr"{input_path}\PROCTIME.xlsx")
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
    df_orderpos=df_orderpos[df_orderpos.Start.isna()]
    df_orders = pd.DataFrame()
    df_orders['Number']=1
    df_orders['WPNo'] = df_orderpos['WPNo']
    df_orders['Order']=df_orderpos['ONo'].astype(str) + '-' + df_orderpos['OPos'].astype(str)
    '''
    # Estrazione della colonna WPNo
    df_orders = df_orderpos["WPNo"]
    # Crea una nuova colonna con valori costanti di 1
    new_column = pd.Series(1, index=df_orders.index, name="Number")
    # Aggiungi la nuova colonna al DataFrame
    df_orders = pd.concat([new_column, df_orders], axis=1)
    '''
    # Esportare la tabella in un file Excel
    df_orders.to_excel(fr"{input_path}\Order_Table.xlsx", index=False)
    print(f"Order_Table has been created")
    return df_orders

'''
def planned_orders_simplified():
    with open('config.json') as f:
        paths = json.load(f)
        input_path = paths['input_path']
    df_orderpos = pd.read_excel(fr"{input_path}\MESb.xlsx", sheet_name="tblOrderPos")
    df_orderpos=df_orderpos[df_orderpos.Start.isna()]
    df = pd.DataFrame()
    df['Number']=1
    df['WPNo'] = df_orderpos['WPNo']
    df['Order']=df_orderpos['ONo'].astype(str) + '-' + df_orderpos['OPos'].astype(str)
    df.to_excel(fr"{input_path}\Order_Table.xlsx", index=False)
    return df
'''