import random
import pandas
import numpy as np
from predictmodel import forecast_RUL as RUL
from sklearn.preprocessing import PolynomialFeatures
from scipy.stats import t


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
c_p = 1

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


tests = 1000
costs = np.zeros(tests)
inspection_schedule = 200
adaptor = 0



for i in range(tests):
    bat = battery(0,random.choice(b_test))
    cost = 0
    for j in range(2000//inspection_schedule):
        bat.cycle_to_inspection(inspection_schedule)
        cost += bat.inspection(inspection_schedule,adaptor)

    costs[i] = cost
    
m = costs.mean()
s = costs.std()

print('Mean =',m,'\nStandard deviaton =',s,'\n')

costs = sorted(costs)

for percentile in [0.01,0.05,0.1,0.25,0.5,0.75,0.9,0.95,0.99]:
    print(percentile,costs[int(tests*percentile)])



        