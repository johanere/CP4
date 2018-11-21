
import numpy as np
import matplotlib.pyplot as plt
import string as str
from matplotlib.pyplot import figure
outdata=["T1ord20","T1rnd20","T23ord20","T23rnd20"]
lab=["ordered", "random","ordered", "random"]


figure(num=None, figsize=(9, 6), dpi=80, facecolor='w', edgecolor='k')
plt.ticklabel_format(axis='both', style='sci')

f, axarr = plt.subplots(2, 2, sharex='all')
#open for reading
for j in range(len(outdata)):
    f= open(outdata[j])
    if f.mode == 'r':
        lines = f.readlines()
    n=len(lines)
    print n
    
    #placeholders
    mcs=np.zeros(n)
    T=np.zeros(n)
    E_avr=np.zeros(n)
    C=np.zeros(n)
    Mtot=np.zeros(n)
    X=np.zeros(n)
    Mabs_avr=np.zeros(n)
    configs=np.zeros(n)
    
    
    #extract data
    for i in range(n):
        hold=lines[i].split()
        mcs[i]=float(hold[0])
        T[i]=float(hold[1])
        E_avr[i]=float(hold[2])
        C[i]=float(hold[3])
        Mtot[i]=float(hold[4])
        X[i]=float(hold[5])
        Mabs_avr[i]=float(hold[6])

    axarr[0,0].scatter(T,E_avr,label="L=%s"%lab[i])
    axarr[0,0].plot(T,E_avr)
    
    axarr[0,1].scatter(T,C,label="L=%s"%lab[i])
    axarr[0,1].plot(T,C)
    
    axarr[1,0].scatter(T,Mabs_avr,label="L=%s"%lab[i])
    axarr[1,0].plot(T,Mabs_avr)
    
    axarr[1,1].scatter(T,X,label="L=%s"%lab[i])
    axarr[1,1].plot(T,X)
    
for i in range(2):
    for j in range(2):
        axarr[i,j].set_xlabel('$k_B T$')
        axarr[i,j].grid(True, linestyle='-.')
        axarr[i,j].legend()
axarr[0,0].set_ylabel('$<E>/L^2$')
axarr[0,1].set_ylabel('$C_V$' )
axarr[1,0].set_ylabel('$<|M|>$' )
axarr[1,1].set_ylabel('$\chi$' )

plt.show()


