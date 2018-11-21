%%matlab program to calculate analytical solutions for 2x2 lattice as function of T

k=1%.4e-23;
T=1;
b=1/(k*T);

Z=12+4*cosh(8*b);
E=16/Z*(exp(-8*b)-exp(8*b));
M=8/Z*(exp(8*b)+2);
X=1/b*32/Z*(exp(8*b)+1);
C=1/b/T*(256/Z*cosh(8*b)-E^2);
C=1/b/T*(128/Z*(exp(-8*b)+exp(8*b))-E^2);

Z
E=E/4
M=M/4
X=X/4
C=C/4

(-1.9961-E)/(E)
(3.995-X)/(X)
