#!/bin/bash
#SBATCH -A 128cores
#SBATCH --job-name=RascalC
#SBATCH --output=/home/ataverna/outRascalCs.txt
#SBATCH --error=/home/ataverna/errorRascalC.txt
###SBATCH --nodes=4
#
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=64
##SBATCH --time=24:00:00
#SBATCH --nodelist=miclap

### Configurar OpenMP/MKL/etc con la cantidad de cores detectada.
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export MKL_NUM_THREADS=$SLURM_CPUS_PER_TASK
export NUMEXPR_NUM_THREADS=$SLURM_CPUS_PER_TASK
export NUMEXPR_MAX_THREADS=64


##fixedAmp_002 ----------------------------------
##python3 python/xi_estimator_periodic_mod.py #para nd1_00
##python3 python/xi_estimator_periodic.py ../den_files/mass_cuts_nd1_00_z0_fixedAmp_002.txt radial_binning_corr.csv 1000. 1. 20 64 output/nd1_00/
##python python/xi_estimator_periodic.py ../den_files/mass_cuts_nd3_00_z0_fixedAmp_002.txt radial_binning_corr.csv 1000 1. 20 8 output/nd3_00/

##python python/compute_correction_function.py ../den_files/mass_cuts_nd1_00_z0_fixedAmp_002.txt radial_binning_cov.csv output/nd1_00/ 1
##python python/compute_correction_function.py ../den_files/mass_cuts_nd3_00_z0_fixedAmp_002.txt radial_binning_cov.csv output/nd3_00/ 1

##make
##./cov -def

##python python/post_process_legendre.py output/nd1_00/ 25 0 10 output/nd1_00/ 1.
##python python/post_process_legendre.py output/nd3_00/ 25 2 10 output/nd3_00/ 1.

python python/convert_xi_to_multipoles.py output/nd1_00/xi_n200_m20_periodic_11.dat 0 output/nd1_00/xi_to_multipoles.dat
##python python/convert_xi_to_multipoles.py output/nd3_00/xi_n200_m20_periodic_11.dat 0 output/nd3_00/xi_to_multipoles.dat
