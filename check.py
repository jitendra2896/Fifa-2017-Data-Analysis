import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_table("FullData.csv",sep=",")

x = df['Ball_Control'].tolist()
print(x)
