import numpy as np
from pathlib import Path
import src.helpers as helpers
import src.analysis as analysis

def read(folder):
    datavec = []
    folder_path = Path(folder)
  
    if not folder_path.exists():
        raise FileNotFoundError(f"{folder} does not exist")
    
    for file in folder_path.glob("*.txt"):
        # ignore test.txt
        if file.name == r"test.txt":
            continue

        data = np.loadtxt(file, dtype=str)
        datavec.append(data)
    
    # Step 1 -> make timeseries
    clean_datavec = []
    for data in datavec:
        clean_data = []
        for idx, row in enumerate(data):
            n_value = helpers.date_to_n(row[0])
            p_value = float(row[4])
            clean_data.append( [n_value, p_value] )
        clean_datavec.append(clean_data)

    # Step 2 -> unzip, flip and interpolate
    temp_datavec = []
    for data in clean_datavec:
        n_vals, p_vals = zip(*data) 
        n_vals, p_vals = n_vals[::-1], p_vals[::-1] 
        n_vals, p_vals = analysis.fill_blanks(n_vals, p_vals)
        temp_datavec.append([n_vals, p_vals])

    L = helpers.days_since_start()
    n = list( range(L) )
    p = [0] * L

    # Step 3 -> combine all data, data = [ [n1, p1], [n2, p2], ... etc ]
    for data in temp_datavec: 
        n_vals = data[0]
        p_vals = data[1]
        l = len(n_vals)
        
        for i in range(l):
            if p[ n_vals[i] ] == 0:
                p[ n_vals[i] ] = float( p_vals[i] )
    
    # Remove potential zeros at the end of the price array
    for di in reversed(range(L)):
        if(p[di] == 0):
            p.pop(di)
            n.pop(di)
    
    
    length = len(n)

    # return clean_datavec[0]
    return n, p, length


