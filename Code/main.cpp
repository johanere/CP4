/*
Program to solve the two-dimensional Ising model
18
with zero external field and no parallelization using the Mersenne twister engine for generating random
numbers.
The coupling constant J = 1
Boltzmann’s constant = 1, temperature has thus dimension energy
Metropolis sampling is used. Periodic boundary conditions.
The code needs an output file on the command line and the variables mcs, nspins,
initial temp, final temp and temp step.
Run as
./executable Outputfile numberof spins number of MC cycles initial temp final temp tempstep
./test.x Lattice 100 10000000 2.1 2.4 0.01
Compile and link as
c++ -O3 -std=c++11 -Rpass=loop-vectorize -o Ising.x IsingModel.cpp -larmadillo
*/
#include <cmath>
#include <iostream>
#include <fstream>
#include <iomanip>
#include <cstdlib>
#include <random>
#include <armadillo>
#include <string>
using namespace std;
using namespace arma;
// output file
ofstream ofile;
// inline function for periodic boundary conditions
inline int periodic(int i, int limit, int add)
{
return (i+limit+add) % (limit);
}
// Function to initialise energy and magnetization
void InitializeLattice(int, mat &, double&, double&);
// The metropolis algorithm including the loop over Monte Carlo cycles
void MetropolisSampling(int, int, double, vec &);
// prints to file the results of the calculations
void output(int, int, double, vec);
// Main program begins here
int main(int argc, char* argv[])
{
  string filename;
  int NSpins, MCcycles;
  double InitialTemp, FinalTemp, TempStep;
  if (argc <= 5)
  {
    cout << "Bad Usage: " << argv[0] <<
    " read output file, Number of spins, MC cycles, initial and final temperature and tempurate step" << endl;
    exit(1);
  }
  if (argc > 1)
  {
    filename=argv[1];
    NSpins = atoi(argv[2]);
    MCcycles = atoi(argv[3]);
    InitialTemp = atof(argv[4]);
    FinalTemp = atof(argv[5]);
    TempStep = atof(argv[6]);
  }
  // Declare new file name and add lattice size to file name
  string fileout = filename;
  string argument = to_string(NSpins);

  fileout.append(argument);
  ofile.open(fileout);
  // Start Monte Carlo sampling by looping over T first
  for (double Temperature = InitialTemp; Temperature <= FinalTemp; Temperature+=TempStep)
  {
    vec ExpectationValues = zeros<mat>(5);
    // start Monte Carlo computation
    MetropolisSampling(NSpins, MCcycles, Temperature, ExpectationValues);
    output(NSpins, MCcycles, Temperature, ExpectationValues);
  }
  ofile.close(); // close output file
  return 0;
}
// function to initialise energy, spin matrix and magnetization
void InitializeLattice(int NSpins, mat &SpinMatrix, double& Energy, double& MagneticMoment)
{
  // setup spin matrix and initial magnetization
  for(int x =0; x < NSpins; x++)
  {
    for (int y= 0; y < NSpins; y++)
    {
      SpinMatrix(x,y) = 1.0; // spin orientation for the ground state
      MagneticMoment += (double) SpinMatrix(x,y);
    }
  }
  // setup initial energy
  for(int x =0; x < NSpins; x++)
  {
    for (int y= 0; y < NSpins; y++)
    {
      Energy -= (double) SpinMatrix(x,y)*
      (SpinMatrix(periodic(x,NSpins,-1),y) +
      SpinMatrix(x,periodic(y,NSpins,-1)));
    }
  }
}// end function initialise

// The Monte Carlo part with the Metropolis algo with sweeps over the lattice
void MetropolisSampling(int NSpins, int MCcycles, double Temperature, vec &ExpectationValues)
{
  // Initialize the seed and call the Mersenne algo
  std::random_device rd;
  std::mt19937_64 gen(rd());
  // Then set up the uniform distribution for x \in [[0, 1]
  std::uniform_real_distribution<double> distribution(0.0,1.0);
  // Allocate memory for spin matrix
  mat SpinMatrix = zeros<mat>(NSpins,NSpins);
  // initialise energy and magnetization
  double Energy = 0.; double MagneticMoment = 0.;
  // initialize array for expectation values
  InitializeLattice(NSpins, SpinMatrix, Energy, MagneticMoment);
  // setup array for possible energy changes
  vec EnergyDifference = zeros<mat>(17);
  for( int de =-8; de <= 8; de+=4) EnergyDifference(de+8) = exp(-de/Temperature);
  for (int cycles = 1; cycles <= MCcycles; cycles++)
  {
    // The sweep over the lattice, looping over all spin sites
    for(int x =0; x < NSpins; x++)
    {
      for (int y= 0; y < NSpins; y++)
      {
        int ix = (int) (distribution(gen)*(double)NSpins);
        int iy = (int) (distribution(gen)*(double)NSpins);
        int deltaE = 2*SpinMatrix(ix,iy)*
        (SpinMatrix(ix,periodic(iy,NSpins,-1))+
        SpinMatrix(periodic(ix,NSpins,-1),iy) +
        SpinMatrix(ix,periodic(iy,NSpins,1)) +

        SpinMatrix(periodic(ix,NSpins,1),iy));
        if ( distribution(gen) <= EnergyDifference(deltaE+8) )
        {
          SpinMatrix(ix,iy) *= -1.0; // flip one spin and accept new spin config
          MagneticMoment += (double) 2*SpinMatrix(ix,iy);
          Energy += (double) deltaE;
        }
      }
    }
    // update expectation values for local node
    ExpectationValues(0) += Energy; ExpectationValues(1) += Energy*Energy;
    ExpectationValues(2) += MagneticMoment;
    ExpectationValues(3) += MagneticMoment*MagneticMoment;
    ExpectationValues(4) += fabs(MagneticMoment);
  }
} // end of Metropolis sampling over spins
void output(int NSpins, int MCcycles, double temperature, vec ExpectationValues)
{
  double norm = 1.0/((double) (MCcycles)); // divided by number of cycles
  double E_ExpectationValues = ExpectationValues(0)*norm;
  double E2_ExpectationValues = ExpectationValues(1)*norm;
  double M_ExpectationValues = ExpectationValues(2)*norm;
  double M2_ExpectationValues = ExpectationValues(3)*norm;
  double Mabs_ExpectationValues = ExpectationValues(4)*norm;
  // all expectation values are per spin, divide by 1/NSpins/NSpins
  double Evariance = (E2_ExpectationValues- E_ExpectationValues*E_ExpectationValues)/NSpins/NSpins;
  double Mvariance = (M2_ExpectationValues - Mabs_ExpectationValues*Mabs_ExpectationValues)/NSpins/NSpins;
  ofile << setiosflags(ios::showpoint | ios::uppercase);
  ofile << setw(15) << setprecision(8) << temperature;
  ofile << setw(15) << setprecision(8) << E_ExpectationValues/NSpins/NSpins;
  ofile << setw(15) << setprecision(8) << Evariance/temperature/temperature;
  ofile << setw(15) << setprecision(8) << M_ExpectationValues/NSpins/NSpins;
  ofile << setw(15) << setprecision(8) << Mvariance/temperature;
  ofile << setw(15) << setprecision(8) << Mabs_ExpectationValues/NSpins/NSpins << endl;
} // end output function
