import pandas
import matplotlib.pyplot as plt
a= pandas.read_csv("Battery_train.csv")

#Figure 1 and data table in kernel
display(a)
exclude = ["Cycle"]
a.loc[:, a.columns.difference(exclude)].plot(legend=None)

T = []
for i in range(1,80):
    for j in range(2058):
        if str(a.iloc[j,i]) == "nan":
            break
    T += [j+1]

RUL = []
for i in T:
    temp = []
    for j in range(i):
        temp += [i - j]
    RUL += [temp]
    
CAP = []
for i in range(len(T)):
    temp2 = []
    for j in range(T[i]):
        temp2 += [a.iloc[j,i+1]]
    CAP += [temp2]

##Figure 2
plt.figure()
for k in range(79):
    plt.plot(CAP[k], RUL[k])
plt.xlabel('Capacity C_t,i (Ah)')
plt.ylabel('RUL_t,i (Cycles)')
plt.show

##Figure 3
c = pandas.read_csv("Battery_test.csv")
exclude = ["Cycle"]
c.loc[:,c.columns.difference(exclude)].plot(legend=None)
plt.axhline(y=0.88,color='r')
plt.xlabel('t(cycles)')
plt.ylabel('Capacity C_t,i (Ah)')
plt.show
