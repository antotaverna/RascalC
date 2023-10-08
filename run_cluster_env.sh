#!/bin/bash
#SBATCH -A 128cores
#SBATCH --job-name=RascalC
#SBATCH --output=/home/ataverna/outRascalC_env.txt
#SBATCH --error=/home/ataverna/errorRascalC_env.txt
###SBATCH --nodes=4
#
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=96
##SBATCH --time=24:00:00
##SBATCH --nodelist=miclap
#SBATCH --nodelist=taurus

### Configurar OpenMP/MKL/etc con la cantidad de cores detectada.
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export MKL_NUM_THREADS=$SLURM_CPUS_PER_TASK
export NUMEXPR_NUM_THREADS=$SLURM_CPUS_PER_TASK
export NUMEXPR_MAX_THREADS=96


##fixedAmp_002 ----------------------------------
##python3 python/xi_estimator_periodic.py ../env_files/voids_pweb_z0_fixedAmp_002.txt radial_binning_corr.csv 1000. 1. 20 64 output/env_pweb/
##python3 python/xi_estimator_periodic.py ../env_files/sheets_pweb_z0_fixedAmp_002.txt radial_binning_corr.csv 1000. 1. 20 64 output/env_pweb/
##python3 python/xi_estimator_periodic.py ../env_files/knots_pweb_z0_fixedAmp_002.txt radial_binning_corr.csv 1000. 1. 20 64 output/env_pweb/
##python3 python/xi_estimator_periodic.py ../env_files/filaments_vweb_z0_fixedAmp_002.txt radial_binning_corr.csv 1000. 1. 20 64 output/env_vweb/
##python3 python/xi_estimator_periodic_mod.py

##--------------------correction_function
##knots
##python python/compute_correction_function.py ../env_files/randoms_5x_knots_pweb_z0_fixedAmp_002.txt radial_binning_cov_60_160.csv output/env_pweb/ 1
##python python/compute_correction_function.py ../env_files/randoms_5x_knots_pweb_z0_fixedAmp_002.txt radial_binning_cov_60_160.csv output/env_vweb/ 1
##sheets
##python python/compute_correction_function.py ../env_files/randoms_5x_sheets_pweb_z0_fixedAmp_002.txt radial_binning_cov_60_160.csv output/env_pweb/ 1
##python python/compute_correction_function.py ../env_files/randoms_5x_sheets_pweb_z0_fixedAmp_002.txt radial_binning_cov_60_160.csv output/env_vweb/ 1
##filaments
##python python/compute_correction_function.py ../env_files/randoms_5x_filaments_pweb_z0_fixedAmp_002.txt radial_binning_cov_60_160.csv output/env_pweb/ 1
##voids 2x
##python python/compute_correction_function.py ../env_files/randoms_2x_voids_pweb_z0_fixedAmp_002.txt radial_binning_cov_60_160.csv output/env_pweb/ 1

##first 2x
##python python/compute_correction_function.py ../env_files/randoms_2x_centros_n_50_z0_fixedAmp_002.txt radial_binning_cov_60_160.csv output/first/ 1



###---------------------------------------------------------------------
##make
##./cov -def

##python python/post_process_legendre.py output/first/ 25 0 30 output/first/ 1.
##python python/post_process_legendre.py output/env_pweb/ 25 0 30 output/env_pweb/ 1.
##python python/post_process_legendre.py output/env_vweb/ 25 0 30 output/env_vweb/ 1.


##python python/convert_xi_to_multipoles.py output/env_pweb/xi_n200_m20_periodic_11.dat 0 output/env_pweb/xi_to_multipoles.dat
##python python/convert_xi_to_multipoles.py output/first/xi_n200_m20_periodic_11_2x.dat 0 output/first/xi_to_multipoles.dat
