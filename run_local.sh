conda activate nbodykit-env

python python/write_binning_file_linear.py 25 25 150 radial_binning_cov.csv
python python/write_binning_file_linear.py 200 0 200 radial_binning_corr.csv

#fixedAmp_001 ----------------------------------
#python python/xi_estimator_periodic.py ../den_files/mass_cuts_nd3_00_z0.txt radial_binning_corr.csv 1000 1. 20 10 xi/
#python python/compute_correction_function.py ../den_files/mass_cuts_nd3_00_z0.txt radial_binning_cov.csv ./ 1
#make
#./cov -def
#python python/post_process_legendre.py output/ 25 2 10 output/ 1.


#fixedAmp_002 ----------------------------------
#python python/xi_estimator_periodic.py {GALAXY_FILE} {RADIAL_BIN_FILE} {BOXSIZE} {MU_MAX} {N_MU_BINS} {NTHREADS} {OUTPUT_DIR} [{GALAXY_FILE_2}]
#python python/xi_estimator_periodic.py ../den_files/mass_cuts_nd1_00_z0_fixedAmp_002.txt radial_binning_corr.csv 1000 1. 20 8 output/nd1_00/
#python python/xi_estimator_periodic.py ../den_files/mass_cuts_nd3_00_z0_fixedAmp_002.txt radial_binning_corr.csv 1000 1. 20 8 output/nd3_00/

#python python/compute_correction_function.py {GALAXY_FILE} {BIN_FILE} {OUTPUT_DIR} {PERIODIC} [{RR_COUNTS}]
#python python/compute_correction_function.py ../den_files/mass_cuts_nd1_00_z0_fixedAmp_002.txt radial_binning_cov.csv output/nd1_00/ 1
#python python/compute_correction_function.py ../den_files/mass_cuts_nd3_00_z0_fixedAmp_002.txt radial_binning_cov.csv output/nd3_00/ 1

make
./cov -def

#python python/post_process_default.py {COVARIANCE_DIR} {N_R_BINS} {N_MU_BINS} {N_SUBSAMPLES} {OUTPUT_DIR} [{SHOT_NOISE_RESCALING}]
#python python/post_process_legendre.py {COVARIANCE_DIR} {N_R_BINS} {MAX_L} {N_SUBSAMPLES} {OUTPUT_DIR} [{SHOT_NOISE_RESCALING}]
python python/post_process_legendre.py output/nd1_00/ 25 0 10 output/nd1_00/ 1.
#python python/post_process_legendre.py output/nd3_00/ 25 2 10 output/nd3_00/ 1.
#(N_SUBSAMPLES == N_LOOPS (parameters.h))

#Computing Legendre Moments of Correlation Functions
#python python/convert_xi_to_multipoles.py {INFILE} {MAX_L} {OUTFILE}
python python/convert_xi_to_multipoles.py output/nd1_00/xi_n200_m20_periodic_11.dat 0 output/nd1_00/xi_to_multipoles.dat
#python python/convert_xi_to_multipoles.py output/nd3_00/xi_n200_m20_periodic_11.dat 0 output/nd3_00/xi_to_multipoles.dat

#Para correr solo l0, primer se modifica el modules/parameters.h y luego se corre asi:
#python python/post_process_legendre.py output/ 25 0 10 output/ 1.

