
import numpy as np
import matplotlib.pyplot as plt
import string as str
outdata="T1_ord20" #data_initial_2

L=20


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
    E[i]=float(hold[2])
    C[i]=float(hold[3])
    Mtot[i]=float(hold[4])
    X[i]=float(hold[5])
    M[i]=float(hold[6])
    
N=float(hold[0])
pow=int(np.log10(N))
  
cutoff=30
analytical=np.asarray([-1.9960,0.9987,3.9933,0.0321])
value=[E,M,X,C]
maxrelerror=np.zeros(4)
for i in range(4):
    err=np.zeros(len(E))
    for j in range(cutoff,int(len(E))):
        err[j]=abs((value[i][j]-analytical[i])/analytical[i])
    maxrelerror[i]=max(err)
print "Max rel errors, E,M,X,C after first 30 percent of cycles"
print maxrelerror
print len(E)
   
#plot
from matplotlib.pyplot import figure
 
figure(num=None, figsize=(9, 6), dpi=80, facecolor='w', edgecolor='k')
plt.ticklabel_format(axis='both', style='sci')
plt.plot(mcs,E) # %s)'%[i])        
plt.xlabel('MC cycles', fontsize=14)
plt.ylabel('$<E>/L^2$', fontsize=14)
plt.grid('on')
plt.title('$<E>$ for $L=%s$, $T=1$ over $10^%s$ Monte Carlo cycles'%(L,pow), fontsize=14)
plt.show()       
 
figure(num=None, figsize=(9, 6), dpi=80, facecolor='w', edgecolor='k')
plt.ticklabel_format(axis='both', style='sci')
plt.plot(mcs,M) # %s)'%[i])        
plt.xlabel('MC cycles',fontsize=14)
plt.ylabel('$<|M|>/L^2$',fontsize=14)
plt.grid('on')
plt.title('$<|M|>$ for $L=%s$, $T=1$ over $10^%s$ Monte Carlo cycles'%(L,pow), fontsize=14)
plt.show()      
 
figure(num=None, figsize=(9, 6), dpi=80, facecolor='w', edgecolor='k')
plt.ticklabel_format(axis='both', style='sci')
plt.plot(mcs,X) # %s)'%[i])        
plt.xlabel('MC cycles',fontsize=14)
plt.ylabel('$\chi$',fontsize=14)
plt.grid('on')
plt.title('$\chi$ for $L=%s$, $T=1$ over $10^%s$ Monte Carlo cycles'%(L,pow), fontsize=14)
plt.show()    
 
figure(num=None, figsize=(9, 6), dpi=80, facecolor='w', edgecolor='k')
plt.ticklabel_format(axis='both', style='sci')
plt.plot(mcs,C) # %s)'%[i])        
plt.xlabel('MC cycles',fontsize=14)
plt.ylabel('$C_V/$ $Jk_b$',fontsize=14)
plt.grid('on')
plt.title('$C_V$ for $L=%s$, $T=1$ over $7 \cdot 10^%s$ Monte Carlo cycles'%(L,pow), fontsize=14)
plt.show()    
