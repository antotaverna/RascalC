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
python3 output/2pcf_pycorr_nden.py
