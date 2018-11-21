
import numpy as np
import matplotlib.pyplot as plt
import string as str
from matplotlib.pyplot import figure
outdata=["T23ord20","T23rnd20"]
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
        M[i]=float(hold[6])

        

    #plot
    plt.plot(mcs[30:],M[30:],label="%s"%(lab[j]))       

N=float(hold[0])
pow=int(np.log10(N))


#===============================================================================
# #comparison to analytical for 2x2 
# cutoff=150
# analytical=-1.9960
# err=np.zeros(len(E))
# for j in range(cutoff,int(len(E))):
#     err[j]=abs((M[j]-analytical)/analytical)
#===============================================================================


 
plt.xlabel('MC cycles', fontsize=14)
plt.ylabel('$<|M|>$', fontsize=14)
plt.grid('on')
plt.legend(loc=0)
plt.title('$<|M|>$ for $L=%s$, $T=%s$ over $4 \cdot 10^%s$ Monte Carlo cycles'%(L,T[1],pow), fontsize=14)
plt.show()       
