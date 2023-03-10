import pandas as pd
import matplotlib.pyplot as plt
plt.rc('text.latex', preamble=r'\usepackage{textgreek}')

##Figure 1
a = pd.read_csv("Battery_train.csv")
exclude = ["Cycle"]
a.loc[:, a.columns.difference(exclude)].plot(legend=None)
plt.axhline(y=0.88, color='r')
plt.xlabel(r'$t$ (cycles)')
plt.ylabel(r'Capacity $C_{t,i}$ $(Ah)$')
plt.show()


##Figure 2
T = []
for i in range(1,80):
    for t in range(2058):
        if str(a.iloc[t,i]) == "nan":
            break
    T+=[t+1]

RUL = []
for i in T:
    temp = []
    for j in range(i):
        temp += [i-j]
    RUL += [temp]

CAP = []
for i in range(len(T)):
    temp2 = []
    for j in range(T[i]):
        temp2 += [a.iloc[j,i+1]]
    CAP += [temp2]

plt.figure()
for k in range(79):
    plt.plot(CAP[k], RUL[k])
plt.xlabel(r'Capacity $C_{t,i}$ $(Ah)$')
plt.ylabel(r'$RUL_{t,i}$ (Cycles)')
plt.show()


##Figure 3
b = pd.read_csv("Battery_test.csv")
exclude = ["Cycle"]
b.loc[:,b.columns.difference(exclude)].plot(legend=None)
plt.axhline(y=0.88,color='r')
plt.xlabel(r'$t$ (cycles)')
plt.ylabel(r'Capacity $C_{t,i}$ $(Ah)$')
plt.show()


##Figure 4
T2 = []
for i in range(1,11):
    for t in range(1696):
        if str(b.iloc[t,i]) == "nan":
            break
    T2+=[t+1]

RUL2 = []
for i in T2:
    temp = []
    for j in range(i):
        temp += [i-j]
    RUL2 += [temp]

CAP2 = []
for i in range(len(T2)):
    temp2 = []
    for j in range(T2[i]):
        temp2 += [b.iloc[j,i+1]]
    CAP2 += [temp2]


plt.figure()
for k in range(10):
    plt.plot(CAP2[k], RUL2[k])
plt.xlabel(r'Capacity $C_{t,i}$ $(Ah)$')
plt.ylabel(r'$RUL_{t,i}$ (Cycles)')
plt.show()
