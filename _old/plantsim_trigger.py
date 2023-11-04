import os
import re
import time
import json
import numpy as np
import pandas as pd
from plantsim.plantsim import Plantsim
from plantsim.table import Table

def plantsim_trigger():
    with open('config.json') as f:
        paths = json.load(f)
        model_path = paths['model_path']
        output_path = paths['output_path']
    plantsim = Plantsim(version = '16.0', license_type='Student')
    plantsim.load_model(model_path)
    plantsim.set_path_context('.Models.Model')
    plantsim.set_event_controller()
    plantsim.reset_simulation()
    plantsim.start_simulation()

    filename = "FinishTimes.xlsx"
    output_path = os.path.join(output_path, filename)
    
    while not os.path.exists(output_path):
        pass

    print(f"Il file nella cartella {output_path} è stato generato.")
    plantsim.quit()