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
        # temporary comment for testing
        if file.name == r"test.txt":
            continue
        data = np.loadtxt(file, dtype=str)
        datavec.append(data)
    
    clean_datavec = []
    for data in datavec:
        clean_data = []
        for idx, row in enumerate(data):
            n = helpers.date_to_n(row[0])
            p = float(row[4])
            clean_data.append( [n, p] )

        clean_datavec.append(clean_data)

    temp_datavec = []
    for data in clean_datavec:
        n, p = zip(*data) 
        n, p = analysis.fill_blanks(n[::-1], p[::-1]) # flip to correct orientation
        temp_datavec.append([n, p])

    n, p = [], []
    for data in temp_datavec:
        #merge all the data in datavec
        pass

    print()
    print("datavec: \n", datavec)
    print()
    print("clean_datavec: \n", clean_datavec[0])
    return clean_datavec[0]


