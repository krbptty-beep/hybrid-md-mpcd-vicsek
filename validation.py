import importlib.metadata
import os
import csv 
import sys

csv.field_size_limit(sys.maxsize)
try:
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    
    print(f"pandas version: {pd.__version__}")
    gsd_version = importlib.metadata.version("gsd")
    print(f"gsd version: {gsd_version}")
    print(f"numpy version: {np.__version__}")
    
    
except ModuleNotFoundError as e:
    
    print(f"Error: Required module '{e.name}' is not installed in this environment.")
    print("Please make sure you have added it via your package manager (e.g., 'pixi add').")
    
    
    raise SystemExit(1)

matplotlib.use('TkAgg')
#df = pd.read_csv("./Plot_data/cluster_validation.csv")
#print(df.head())
x = []
y = []
z = []
with open("./Plot_data/cluster_validation.csv") as avg_mass:
    csvreader = csv.DictReader(avg_mass)
    data_list = dict()
    i = 0
    for row in csvreader:
        if i >= 100:
            break
        if i != 0:
            x.append(round(float(row['timestep']),5))
            y.append(round(float(row['average_mass']),5))
            cluster = row['cluster_mass_dict']
            data = ""
            for s in range(0,len(cluster)):
                print("running")
                if cluster[s]=="{":
                    print("running2")
                    S = 6
                    while S <= 11:
                        data+=cluster[s+S] 
                        print(data) 
                        S+=1
                        
                break
            z.append(float(data))
        i+=1

#y = round(y,5)
print("x:")
print(len(x))
print("y:")
print(len(y))
print("z:")
print(z)

plt.figure(figsize=(10,5))
plt.plot(x,y)

plt.title("average mass vs time")
plt.xlabel("time" , fontsize = 12)
plt.ylabel("average mass", fontsize = 12)

plt.savefig('./Plot_data/average_mass.png')
plt.close()

##==plot2
plt.figure(figsize=(10,5))
plt.plot(x,z)

plt.title("cluster mass vs time")
plt.xlabel("time" , fontsize = 12)
plt.ylabel("cluster mass", fontsize = 12)

plt.savefig('./Plot_data/cluster0_mass.png')
