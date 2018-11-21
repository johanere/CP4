
import numpy as np
import matplotlib.pyplot as plt
import string as str
from matplotlib.pyplot import figure
outdata="T1_T23_20"
L=20

figure(num=None, figsize=(9, 6), dpi=80, facecolor='w', edgecolor='k')
plt.ticklabel_format(axis='both', style='sci')

#open for reading

f= open(outdata)
if f.mode == 'r':
    lines = f.readlines()
n=len(lines)

#placeholders
mcs=np.zeros(n)
T=np.zeros(n)
E=np.zeros(n)
C=np.zeros(n)
Mtot=np.zeros(n)
X=np.zeros(n)
M=np.zeros(n)
configs=np.zeros(n)

#extract data
for i in range(len(lines)):
    hold=lines[i].split()
    mcs[i]=float(hold[0])
    T[i]=float(hold[1])
    configs[i]=float(hold[7])

#plot
plt.plot(T,configs/mcs)   

N=float(hold[0])
pow=int(np.log10(N))  
plt.ylabel('MC cycles',fontsize=14)
plt.xlabel('$k_b T$',fontsize=14)
plt.grid('on')
plt.title('Average accepted spins per sweep for $L=%s$, over $k_B T=[1, 2.4]$ with $4 c\dot 10^%s$ cycles'%(L,pow), fontsize=14)
plt.show()      

