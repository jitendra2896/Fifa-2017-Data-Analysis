
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import glob as gb

dfclubnames = pd.read_csv('ClubNames.csv')
dffullnames = pd.read_csv('FullData.csv')
dfnationalnames = pd.read_csv('NationalNames.csv')
dfplayernames = pd.read_csv('PlayerNames.csv')

ws=dffullnames.loc[:1000,('Name','Nationality','Long_Shots','Freekick_Accuracy','Penalties','Stamina','Crossing','Shot_Power','Finishing')]

sns.lmplot(x='Crossing', y='Stamina', data=ws)
plt.title('Stamina vs Crossing')
plt.show()

sns.lmplot(x='Long_Shots', y='Shot_Power', data=ws)
plt.title('Long Shots vs Shot Power')
plt.show()

sns.lmplot(x='Freekick_Accuracy', y='Stamina', data=ws)
plt.title('Freekick_Accuracy vs Stamina')
plt.show()

sns.lmplot(x='Finishing', y='Penalties', data=ws)
plt.title('Finishing vs Penalties')
plt.show()
'''
plt.scatter(ws['Crossing'], ws['Stamina'], label='data', color='red', marker='o')
sns.regplot(x='Crossing', y='Stamina', data=ws, order=7)

sns.residplot(x='Crossing', y='Stamina',data=ws,color='indianred')

wsl10=ws[-10:]
plt.subplot(2,2,1)
sns.stripplot(x='Long_Shots', y='Nationality', data=wsl10)
plt.ylabel('Nationality')

plt.subplot(2,2,2)
sns.stripplot(x='Penalties', y='Name', data=wsl10, jitter=True , size=3)
plt.ylabel('Name')
plt.tight_layout()

plt.show()

sns.swarmplot(x='Penalties',y='Nationality',data=wsl10)
plt.title('Penalitties vs Nationality')
plt.show()


plt.axis([0,130,0,15])
sns.swarmplot(x='Penalties',y='Nationality',data=wsl10,hue='Name', color='red')
plt.legend(loc=5)
plt.tight_layout()
plt.show()

sns.jointplot(x='Freekick_Accuracy',y='Long_Shots',data=ws, kind='scatter', color='r')

sns.jointplot(x='Freekick_Accuracy',y='Long_Shots',data=ws, kind='hex', color='g')

sns.jointplot(x='Freekick_Accuracy',y='Long_Shots',data=ws, kind='resid')

plt.tight_layout()

cmap = sns.cubehelix_palette(light=.8, as_cmap=True)
sns.jointplot(x='Freekick_Accuracy',y='Long_Shots',data=ws, kind='kde',cmap=cmap, shade=True)
sns.jointplot(x='Freekick_Accuracy',y='Long_Shots',data=ws, kind='reg')
plt.show()

wsf10=ws.loc[:10]
wsf10
sns.pairplot(wsf10, hue='Name', kind='reg')'''