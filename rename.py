import os
import pandas as pd

data_dir = os.path.dirname(os.path.realpath(__file__)) + "\datasets"

filelist = []
for (dirpath, dirnames, filenames) in os.walk(data_dir):
    for f in filenames:
        filepath = dirpath + '\\' +f
        filelist.append(filepath)

for f in filelist:
    df = pd.read_csv(f)
    os.rename(f, f.rsplit('_', 1)[0] + '_' + str(df.shape[0])+'.csv')