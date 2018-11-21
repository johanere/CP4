
import numpy as np
import matplotlib.pyplot as plt
import string as str
from matplotlib.pyplot import figure
outdata=["T1ord20","T1rnd20","T23ord20","T23rnd20"]
lab=["ordered T=1", "randomT=1","ordered T=2.3", "random T=2.3",]
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
        M[i]=float(hold[6])
        
        avraftereq=sum(M[300:400])/100.0
    #plot
    plt.plot(mcs[20:],M[20:]/avraftereq,label="%s"%(lab[j]))   

plt.xlabel('MC cycles',fontsize=14)
plt.ylabel('$<|M|>/<|M|>_{EQ}$',fontsize=14)
plt.grid('on')
plt.legend(loc=0)
plt.title('$<|M|>$ convergence to equilibrium for $L=%s$'%(L), fontsize=14)
plt.show()      

