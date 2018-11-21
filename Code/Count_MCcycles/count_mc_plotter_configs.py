
import numpy as np
import matplotlib.pyplot as plt
import string as str
from matplotlib.pyplot import figure
outdata=["T1ord20","T1rnd20"]
#outdata=["T23ord20","T23rnd20"]
lab=["ordered", "random"]
L=20

figure(num=None, figsize=(9, 6), dpi=80, facecolor='w', edgecolor='k')
plt.ticklabel_format(axis='both', style='sci')

#open for reading
for j in range(len(outdata)):
    f= open(outdata[j])
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
    plt.plot(mcs[30:],configs[30:]/mcs[30:],label="%s, T=%s"%(lab[j],T[1]))   

N=float(hold[0])
pow=int(np.log10(N))  

plt.xlabel('MC cycles',fontsize=14)
plt.ylabel('configurations per sweep',fontsize=14)
plt.grid('on')
plt.legend(loc=0)
plt.title('Number of accepted spins per sweep for $L=%s$, $T=1$ over $10^%s$ Monte Carlo cycles'%(L,pow), fontsize=14)
plt.show()      

