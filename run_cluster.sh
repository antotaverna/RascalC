#!/bin/bash
#SBATCH -A 128cores
#SBATCH --job-name=RascalC
#SBATCH --output=/home/ataverna/outRascalC.txt
#SBATCH --error=/home/ataverna/errorRascalC.txt
###SBATCH --nodes=4
#
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=64
##SBATCH --time=24:00:00
##SBATCH --nodelist=miclap
#SBATCH --nodelist=taurus

### Configurar OpenMP/MKL/etc con la cantidad de cores detectada.
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export MKL_NUM_THREADS=$SLURM_CPUS_PER_TASK
export NUMEXPR_NUM_THREADS=$SLURM_CPUS_PER_TASK
export NUMEXPR_MAX_THREADS=64


##fixedAmp_002 ----------------------------------
## nd1_00
##python3 python/xi_estimator_periodic_mod.py
## nd3_00
##python3 python/xi_estimator_periodic.py ../den_files/mass_cuts_nd1_00_z0_fixedAmp_002.txt radial_binning_corr.csv 1000. 1. 20 64 output/nd1_00/
##python3 python/xi_estimator_periodic_mod.py

##--------------------correction_function
##nd1
##python python/compute_correction_function_only_periodic.py ../den_files/nd1_00_randoms_10x_fixedAmp_002.txt radial_binning_cov_60_160.csv output/nd1_00/ 1
##python python/compute_correction_function.py ../den_files/nd1_00_randoms_10x_fixedAmp_002.txt radial_binning_cov_25_150.csv output/nd1_00/ 1

##nd3
##python python/compute_correction_function.py ../den_files/nd3_00_randoms_1x_fixedAmp_002.txt radial_binning_cov_60_160.csv output/nd3_00/ 1
##python python/compute_correction_function.py ../den_files/nd3_00_randoms_2x_fixedAmp_002.txt radial_binning_cov_60_160.csv output/nd3_00/ 1
##python python/compute_correction_function.py ../den_files/nd3_00_randoms_5x_fixedAmp_002.txt radial_binning_cov_60_160.csv output/nd3_00/ 1
##python python/compute_correction_function.py ../den_files/nd3_00_randoms_10x_fixedAmp_002.txt radial_binning_cov_60_160.csv output/nd3_00/ 1

##python python/compute_correction_function.py ../den_files/nd3_00_randoms_1x_fixedAmp_002.txt radial_binning_cov_25_150.csv output/nd3_00/ 1
##python python/compute_correction_function.py ../den_files/nd3_00_randoms_2x_fixedAmp_002.txt radial_binning_cov_25_150.csv output/nd3_00/ 1
##python python/compute_correction_function.py ../den_files/nd3_00_randoms_5x_fixedAmp_002.txt radial_binning_cov_25_150.csv output/nd3_00/ 1
##python python/compute_correction_function.py ../den_files/nd3_00_randoms_10x_fixedAmp_002.txt radial_binning_cov_25_150.csv output/nd3_00/ 1

##make
./cov -def

python python/post_process_legendre.py output/nd1_00/ 25 0 30 output/nd1_00/ 1.
##python python/post_process_legendre.py output/nd3_00/ 25 0 30 output/nd3_00/ 1.


##python python/convert_xi_to_multipoles.py output/nd1_00/xi_n200_m20_periodic_11.dat 0 output/nd1_00/xi_to_multipoles.dat
##python python/convert_xi_to_multipoles.py output/nd3_00/xi_n200_m20_periodic_11.dat 0 output/nd3_00/xi_to_multipoles.dat
