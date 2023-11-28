import pandas as pd
import numpy as np
import json

from plantsim.plantsim import Plantsim
from plantsim.table import Table

def running_orders(input_file:str,output_file:str=''):
    with open('config.json') as f:
        paths = json.load(f)
        input_path = paths['input_path']
    tblOrderPos_dataframe=pd.read_excel(input_file, sheet_name="tblOrderPos")
    tblStep_dataframe = pd.read_excel(input_file, sheet_name="tblStep")
    tblOrderPos_dataframe['ONo'] = tblOrderPos_dataframe['ONo'].astype(str)+'-'+tblStep_dataframe['OPos'].astype(str)
    tblStep_dataframe['ONo'] = tblStep_dataframe['ONo'].astype(str)+'-'+tblStep_dataframe['OPos'].astype(str)
    # ONos=tblOrderPos_dataframe.loc[~tblOrderPos_dataframe.Start.isna() & tblOrderPos_dataframe.End.isna(),'ONo'].values
    # tblStep_dataframe = tblStep_dataframe.loc[tblStep_dataframe['ONo'].isin(ONos)]
    for order in tblStep_dataframe['ONo'].unique():
        if tblStep_dataframe.loc[(tblStep_dataframe['ONo']==order) & (tblStep_dataframe['FirstStep']),'Start'].item() is not pd.NaT:
            curstep = tblStep_dataframe.loc[(tblStep_dataframe['ONo']==order) & (tblStep_dataframe['FirstStep']==True),'StepNo'].item()
            nextstep = None
            while True:
                if tblStep_dataframe.loc[(tblStep_dataframe['ONo']==order) & (tblStep_dataframe['StepNo']==curstep),'End'] is not pd.NaT: 
                    nextstep = tblStep_dataframe.loc[(tblStep_dataframe['ONo']==order) & (tblStep_dataframe['StepNo']==curstep),'NextStepNo'].item()
                    curstep = None
                else:
                    break
                if tblStep_dataframe.loc[(tblStep_dataframe['ONo']==order) & (tblStep_dataframe['StepNo']==nextstep),'Start'] is not pd.NaT:
                    curstep = nextstep
                    nextstep = None
                else:
                    break
                if not tblStep_dataframe.loc[(tblStep_dataframe['ONo']==order) & (tblStep_dataframe['StepNo']==curstep),'End'].any():
                    break
            if curstep:
                step = curstep
            else:
                step = nextstep
            tblStep_dataframe.drop(index=tblStep_dataframe.loc[(tblStep_dataframe['ONo']==order) & (tblStep_dataframe['StepNo']!=step)].index,inplace=True)            
        else:
            tblStep_dataframe.drop(index=tblStep_dataframe.loc[(tblStep_dataframe['ONo']==order)].index,inplace=True)            
            pass
    tblStep_dataframe['Start'] = np.where(tblStep_dataframe['Start'].notna(), 1, 0)
    tblStep_dataframe = tblStep_dataframe[['WPNo','ONo','OpNo','ResourceID','Start']]
    if output_file != '':
        tblStep_dataframe.to_excel(output_file, index=False)
    return tblStep_dataframe

if __name__ == '__main__':
    print(running_orders)


'''
def wrong_running_orders():
    with open('config.json') as f:
        paths = json.load(f)
        input_path = paths['input_path']
    tblStep_dataframe = pd.read_excel(fr"{input_path}\MESb.xlsx", sheet_name="tblStep")
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
    df_output.to_excel(fr"{input_path}\WorkInProcess.xlsx", index=False)
    return(df_output)
'''