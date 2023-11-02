import json
import pandas as pd

def Monitoring (data_list, Desired_TH, Desired_CT, Desired_EnCons):
    df = pd.DataFrame(data_list)
    average_data = df.mean().to_dict()
    print("Average Data:", average_data)
    
    average_CT_value = average_data['average_CT']
    average_TH_value = average_data['average_TH']
    average_EnCons_value = average_data['total_energy_consumption']
    TH_var = -(average_TH_value - Desired_TH)/Desired_TH #I added a minus, so that the lowest the best
    CT_var = (average_CT_value - Desired_CT)/Desired_CT #the lowest the best
    EC_var = (average_EnCons_value - Desired_EnCons)/Desired_EnCons #the lowest the best
    minimum = min(TH_var,CT_var,EC_var)
    if minimum == TH_var:
        print("The worst performer is the THROUGHPUT")
        data2 = {
        "Worst Parameter": "THROUGHPUT", 
        "Percentage Variation": -minimum*100
        }
    elif minimum == CT_var:
        print("The worst performer is the CYCLE TIME")
        data2 = {
        "Worst Parameter": "CYCLE TIME", 
        "Percentage Variation": -minimum*100
        }
    else:
        print("The worst performer is the ENERGY CONSUMPTION")
        data2 = {
        "Worst Parameter": "ENERGY CONSUMPTION", 
        "Percentage Variation": -minimum*100
        }
    
     # Scrivi il dizionario nel file JSON
    with open("output.json", "w") as json_file:
        json.dump(data2, json_file)

    # Lettura del file JSON
    with open("output.json", "r") as json_file:
        data2 = json.load(json_file)
    return data2




    
