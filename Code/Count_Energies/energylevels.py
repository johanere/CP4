
import numpy as np
import matplotlib.pyplot as plt
import string as str
from matplotlib.pyplot import figure
outdata="40energies_bins"

L=40
cycles=3005000
eq=3000000
samplings=int(cycles-eq)
print samplings

#open for reading

f= open(outdata)
if f.mode == 'r':
    lines = f.readlines()
n=len(lines)

Energies=[]
#extract Energy bins
for j in range(len(lines)):
    hold=lines[j].split()
    for i in range(len(hold)):
        Energies.append(float(hold[i]))
Energies=np.asarray(Energies)

outdata="40energies_T1"
       
f= open(outdata)
if f.mode == 'r':
    lines = f.readlines()
n=len(lines)

Ecount1=[]
#extract Energies T=1
for j in range(len(lines)):
    hold=lines[j].split()
    for i in range(len(hold)):
        Ecount1.append(float(hold[i]))
Ecount1=np.asarray(Ecount1)
   


outdata="40energies_T23"
       
f= open(outdata)
if f.mode == 'r':
    lines = f.readlines()
n=len(lines)

Ecount23=[]
#extract Energies T=2.3
for j in range(len(lines)):
    hold=lines[j].split()
    for i in range(len(hold)):
        Ecount23.append(float(hold[i]))
Ecount23=np.asarray(Ecount23)


 
norm1=float(sum(Ecount1*Energies))
norm23=float(sum(Ecount23*Energies))
 

E1=[]
for i in range(len(Ecount1)):
    index=int(Ecount1[i])
    for j in range(index):
            E1.append(float(Energies[i]))
 
E23=[]
for i in range(len(Ecount23)):
    index=int(Ecount23[i])
    for j in range(index):
            E23.append(float(Energies[i]))
 
  
E1=np.asarray(E1)
E23=np.asarray(E23)
 
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
mean=sum(Ecount23*Energies)/samplings
sigma = sum(Ecount23*(Energies-mean)**2)/samplings

y=Ecount23
x=Energies

mean = sum(x*y)/samplings
sigma = np.sqrt(sum(y*(x-mean)**2)/samplings)
var23= np.sqrt(2.0156393*2.3*2.3*L*L)
print "total variance T=2.3 from Ising solver"
print var23
print "total variance and mean T=2.3 used in gaussian fit"
print sigma, mean

var1 =0.018117197*L*L
print "total variance T=1from Ising solver"
print np.sqrt(var1)

def Gauss(x, a, x0, sigma):
    return a * np.exp(-(x - x0)**2 / (2 * sigma**2))

popt,pcov = curve_fit(Gauss, x, y, p0=[max(y), mean, sigma])

plt.plot(x, y, 'b+:', label='data')
plt.plot(x, Gauss(x, *popt), 'r-', label='fit')
plt.legend()
plt.title('Fit distribution of energies to Gaussian over 5000 cycles, L=40, T=2.3')
plt.xlabel('Energy')
plt.ylabel('Number of configurations')
plt.show()

f, (ax1,ax2) = plt.subplots(1, 2)
f.subtitle('$P(E)$ for $L=40$, %g cycles after %g cycles (eq.time)'%(samplings,eq), fontsize=14)
  
results, edges = np.histogram(E1, normed=True,bins=28)
binWidth = edges[1] - edges[0]
#print (edges[0]-edges[-1])
ax2.bar(edges[:-1], results*binWidth, binWidth)

 
results, edges = np.histogram(E23, normed=True,bins=384)
#print (edges[0]-edges[-1])
binWidth = edges[1] - edges[0]
ax1.bar(edges[:-1], results*binWidth, binWidth)
 
ax1.set_xlabel('E [J]')
ax2.set_xlabel('E [J]')
ax1.set_ylabel('$P(E)$',fontsize=14)
ax2.set_title('T=1')
ax1.set_title('T=2.3')
  
  
plt.savefig('P(E).png', dpi=300)
 



