import pandas as pd
import matplotlib.pyplot as plt

##Figure 1
a = pd.read_csv("Battery_train.csv")
exclude = ["Cycle"]
a.loc[:, a.columns.difference(exclude)].plot(legend=None)
plt.axhline(y=0.88, color='r')
plt.xlabel('t(cycles)')
plt.ylabel('Capacity C_t,i (Ah)')
plt.show()

##Figure 2
b = a
exclude = ["Cycle"]

T = []
for i in range(1,80):
    for t in range(2058):
        if str(a.iloc[t,i]) == "nan":
            break
    T+=[t+1]

CAP = []
for i in range(1,80):
    temp = []
    for t in range(2058):
        if str(a.iloc[t,i]) != "nan":
            temp += [a.iloc[t,i]]
    CAP += [temp]

t = []
for i in range (1,80):
    temp3 = []
    for k in range(1,2059):
        if str(a.iloc[k,i]) == "nan":
            temp3 += [k]
    t += [temp3]

RUL = []
for i in range(0,79):
    temp2 = []
    for j in t:
        temp2 += [T[i]-j[i]]
    RUL += [temp2]

plt.plot(CAP[-1], RUL[-1])
plt.xlabel('Capacity C_t,i (Ah)')
plt.ylabel('RUL_t,i (Cycles)')
plt.show

##Figure 3
c = pd.read_csv("Battery_test.csv")
exclude = ["Cycle"]
c.loc[:,c.columns.difference(exclude)].plot(legend=None)
plt.axhline(y=0.88,color='r')
plt.xlabel('t(cycles)')
plt.ylabel('Capacity C_t,i (Ah)')
plt.show






