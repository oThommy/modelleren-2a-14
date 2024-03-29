import random
import pandas
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from predictmodel import forecast_RUL as RUL
from sklearn.preprocessing import PolynomialFeatures




a_train = pandas.read_csv("Battery_train.csv")
b_train = []
for i in range(1,80):
    nb = []
    for j in range(2058):
        nb.append(a_train.iloc[j,i])
    nb += 500*['nan']
    b_train.append(nb)
    

a_test = pandas.read_csv("Battery_test.csv")
b_test = []
for i in range(1,11):
    nb = []
    for j in range(1696):
        nb.append(a_test.iloc[j,i])
    nb += 500*['nan']
    b_test.append(nb)

c_m = 0.5
c_r = 3
c_p = 100

class battery:
    def __init__(self,init_cycle,lst):
        self.c_cycle = init_cycle
        self.lst = lst
        self.capacity = self.lst[self.c_cycle]
        # self.measurements = []
    
    def cycle_to_inspection(self,inspection_schedule):
        self.c_cycle += inspection_schedule
        self.capacity = self.lst[self.c_cycle]
        # self.measurements.append(self.capacity)
        
    def inspection(self,inspection_schedule,adaptor):
        cost = c_m
        
        # Check if the battery is still working
        if str(self.capacity) == 'nan':
            cost += c_r + c_p
            self.lst = random.choice(b_test)
            self.c_cycle = 0
            self.capacity = self.lst[self.c_cycle]
        
        #Project whether the battery will still be working the next time it is checked
        elif RUL(self.capacity) < inspection_schedule + adaptor: #+- some number if that reduces cost
            cost += c_r
            self.lst = random.choice(b_test)
            self.c_cycle = 0
            self.capacity = self.lst[self.c_cycle]
            
        return cost

adaptors = []
inspection_schedules = []
costs = []


for adaptor in [0]:
    for inspection_schedule in range(200,501):
        bat = battery(0,random.choice(b_train + b_test))
        cost = 0
        for i in range(1000000//inspection_schedule):
            bat.cycle_to_inspection(inspection_schedule)
            cost += bat.inspection(inspection_schedule,adaptor)
        adaptors.append(adaptor)
        inspection_schedules.append(inspection_schedule)
        costs.append(cost)
        # print('adaptor:',adaptor,'| inspection schedule:',inspection_schedule,'| cost:', cost)

# x = np.reshape(adaptors, (len(set(adaptors)),len(set(inspection_schedules))))
# y = np.reshape(inspection_schedules, (len(set(adaptors)),len(set(inspection_schedules))))
# z = np.reshape(costs, (len(set(adaptors)),len(set(inspection_schedules))))


# fig1 = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# ax.plot_surface(x,y,z)

# ax.set_xlabel('adaptor')
# ax.set_ylabel('inspection_schedule')
# ax.set_zlabel('cost')

plt.figure(2)
plt.scatter(inspection_schedules,costs, s = 5)

min_d, max_d = 80, 80
colors = ['g','r','c','m','y','k']*20
polynomials = []

for d in range(min_d,max_d+1):
    z = np.polyfit(inspection_schedules,costs, d)
    polynomials.append((np.poly1d(z),d))

for (p,d) in polynomials:
    plt.plot(inspection_schedules,p(inspection_schedules),color = colors[d-1],label = 'degree '+str(d))

# plt.legend()
plt.xlabel('Inspection frequency')
plt.ylabel('Cost')


        