
import numpy as np
import matplotlib.pyplot as plt
import string as str
outdata="dataMC"
T=1

#open for reading
f= open(outdata)
if f.mode == 'r':
    lines = f.readlines()
n=len(lines)

#placeholders
mcs=np.zeros(n)
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
    E[i]=float(hold[1])
    C[i]=float(hold[2])
    Mtot[i]=float(hold[3])
    X[i]=float(hold[4])
    M[i]=float(hold[5])
    configs[i]=float(hold[1])
    
N=float(hold[0])

pow=int(np.log10(N))


#plot
from matplotlib.pyplot import figure
figure(num=None, figsize=(9, 6), dpi=80, facecolor='w', edgecolor='k')
plt.plot(mcs,E) # %s)'%[i])        
plt.xlabel('MC cycles', fontsize=14)
plt.ylabel('$<E>/L^2$', fontsize=14)
plt.grid('on')
plt.title('$<E>$ for $T=1$ over $10^%s$ Monte Carlo cycles'%pow, fontsize=14)
plt.show()       

figure(num=None, figsize=(9, 6), dpi=80, facecolor='w', edgecolor='k')
plt.plot(mcs,M) # %s)'%[i])        
plt.xlabel('MC cycles',fontsize=14)
plt.ylabel('$<|M|>/L^2$',fontsize=14)
plt.grid('on')
plt.title('$<|M|>$ for $T=1$ over $10^%s$ Monte Carlo cycles'%pow, fontsize=14)
plt.show()      

figure(num=None, figsize=(9, 6), dpi=80, facecolor='w', edgecolor='k')
plt.plot(mcs,X) # %s)'%[i])        
plt.xlabel('MC cycles',fontsize=14)
plt.ylabel('$\chi$',fontsize=14)
plt.grid('on')
plt.title('$\chi$ for $T=1$ over $10^%s$ Monte Carlo cycles'%pow, fontsize=14)
plt.show()    

figure(num=None, figsize=(9, 6), dpi=80, facecolor='w', edgecolor='k')
plt.plot(mcs,C) # %s)'%[i])        
plt.xlabel('MC cycles',fontsize=14)
plt.ylabel('$C_V/$ $Jk_b$',fontsize=14)
plt.grid('on')
plt.title('$C_V$ for $T=1$ over $10^%s$ Monte Carlo cycles'%pow, fontsize=14)
plt.show()    
