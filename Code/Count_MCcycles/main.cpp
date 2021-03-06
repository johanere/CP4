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
./executable Outputfile <#spins> <"MCcycles> <init temp> <final temp> <tempstep> <#prints> <init_config>(0=random, all other=ordered up)
Compile and link with makefile
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
void MetropolisSampling(int, int, double, vec &,int, int);
// prints to file the results of the calculations
void output(int, int, double, vec,int);
// Main program begins here
int main(int argc, char* argv[])
{
  string filename;
  int NSpins, MCcycles, ptotal, intital_config;
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
    ptotal=atoi(argv[7]); //number of prints to outfile
    intital_config=atoi(argv[8]);
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
    MetropolisSampling(NSpins, MCcycles, Temperature, ExpectationValues,ptotal,intital_config);
  }
  ofile.close(); // close output file
  return 0;
}
// function to initialise energy, spin matrix and magnetization
void InitializeLattice(int NSpins, mat &SpinMatrix, double& Energy, double& MagneticMoment)
{
  // setup initial energy
  for(int x =0; x < NSpins; x++)
  {
    for (int y= 0; y < NSpins; y++)
    {
      Energy -= (double) SpinMatrix(x,y)*
      (SpinMatrix(periodic(x,NSpins,-1),y) +
      SpinMatrix(x,periodic(y,NSpins,-1)));
      MagneticMoment += (double) SpinMatrix(x,y);
    }
  }
}// end function initialise

// The Monte Carlo part with the Metropolis algo with sweeps over the lattice
void MetropolisSampling(int NSpins, int MCcycles, double Temperature, vec &ExpectationValues,int ptotal,int intital_config)
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
  // setup spin matrix and initial magnetization
  for(int x =0; x < NSpins; x++)
  {
    for (int y= 0; y < NSpins; y++)
    {
      SpinMatrix(x,y) = 1.0; // spin orientation for the ground state
    }
  }
  if (intital_config==0) //random initial config if initial config ==0
  {
    cout<<"Initiating with random config"<<endl;
    for(int x =0; x < NSpins; x++)
    {
      for (int y= 0; y < NSpins; y++)
      {
        int ix = (int) (distribution(gen)*(double)NSpins);
        int iy = (int) (distribution(gen)*(double)NSpins);
        SpinMatrix(ix,iy) *= -1.0;
      }
    }
  }
  InitializeLattice(NSpins, SpinMatrix, Energy, MagneticMoment); //init energy and magmom

  // setup array for possible energy changes
  vec EnergyDifference = zeros<mat>(17);
  for( int de =-8; de <= 8; de+=4) EnergyDifference(de+8) = exp(-de/Temperature);

  int accepted_configs=0; //count accepted spin configs
  //set up to partition cycles into print intervals
  int MCs_per_print_cycle=MCcycles/ptotal;
  int cycles=0;
  for (int pcycles=1; pcycles<=ptotal; pcycles++)
  {
    for (;cycles < pcycles*MCs_per_print_cycle; cycles++)
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
            accepted_configs+=1;
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
      output(NSpins, cycles, Temperature, ExpectationValues,accepted_configs);

  }
} // end of Metropolis sampling over spins
void output(int NSpins, int cycles, double temperature, vec ExpectationValues,int accepted_configs)
{
  double norm = 1.0/((double) (cycles)); // divided by number of cycles
  double Etotal_average = ExpectationValues(0)*norm;
  double E2total_average = ExpectationValues(1)*norm;
  double Mtotal_average = ExpectationValues(2)*norm;
  double M2total_average = ExpectationValues(3)*norm;
  double Mabstotal_average = ExpectationValues(4)*norm;
  // all expectation values are per spin, divide by 1/NSpins/NSpins
  double Evariance = (E2total_average- Etotal_average*Etotal_average)/NSpins/NSpins;
  double Mvariance = (M2total_average - Mtotal_average*Mtotal_average)/NSpins/NSpins;
  ofile << setiosflags(ios::showpoint | ios::uppercase);
  ofile << setw(15) << setprecision(8) << cycles;
  ofile << setw(15) << setprecision(8) << temperature;
  ofile << setw(15) << setprecision(8) << Etotal_average/NSpins/NSpins;
  ofile << setw(15) << setprecision(8) << Evariance/temperature/temperature;
  ofile << setw(15) << setprecision(8) << Mtotal_average/NSpins/NSpins;
  ofile << setw(15) << setprecision(8) << Mvariance/temperature;
  ofile << setw(15) << setprecision(8) << Mabstotal_average/NSpins/NSpins;
  ofile << setw(15) << setprecision(8) << accepted_configs<< endl;
} // end output function
