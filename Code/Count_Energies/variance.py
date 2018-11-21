
import numpy as np
import matplotlib.pyplot as plt
import string as str
outdata="energies_T1"

L=40


f= open(outdata)
if f.mode == 'r':
    lines = f.readlines()
n=len(lines)

#extract Energies
hold=lines[0].split()
bins=int(len(hold))
evariance1=np.zeros(bins)
for i in range(len(hold)):
    evariance1[i]=float(hold[i])
        
#extract Energy count for T=1
hold=lines[3].split()
bins=len(hold)
evariance23=np.zeros(bins)
for i in range(len(hold)):
    evariance23[i]=float(hold[i])
    

print "Variance for T=1"
print np.sqrt(evariance1[-1])

print "Variance for T=2.3"
print np.sqrt(evariance23[-1])

