import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

dfclubnames = pd.read_csv('ClubNames.csv')
dffullnames = pd.read_csv('FullData.csv')
dfnationalnames = pd.read_csv('NationalNames.csv')
dfplayernames = pd.read_csv('PlayerNames.csv')

print (dfclubnames)
