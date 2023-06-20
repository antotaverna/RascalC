python python/write_binning_file_linear.py 25 25 150 radial_binning_cov.csv
python python/write_binning_file_linear.py 200 0 200 radial_binning_corr.csv

python python/xi_estimator_periodic.py ../den_files/mass_cuts_nd3_00_z0.txt radial_binning_corr.csv 1000 1. 20 10 xi/

python python/compute_correction_function.py ../den_files/mass_cuts_nd3_00_z0.txt radial_binning_cov.csv ./ 1


make
./cov -def

python python/post_process_legendre.py output/ 25 2 10 output/ 1.


#Para correr solo l0, primer se modifica el modules/parameters.h y luego se corre asi:
#python python/post_process_legendre.py output/ 25 0 10 output/ 1.

