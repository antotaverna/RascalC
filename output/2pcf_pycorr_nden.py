import h5py
import numpy as np

from pycorr import TwoPointCorrelationFunction, setup_logging
#from pycorr import TwoPointEstimator, NaturalTwoPointEstimator, utils
from pycorr import BoxSubsampler
from pycorr import TwoPointCounter, AnalyticTwoPointCounter, NaturalTwoPointEstimator

#import os
#os.environ['NUMEXPR_MAX_THREADS'] = '128'
#os.environ['NUMEXPR_NUM_THREADS'] = '64'
#import numexpr as ne

# To activate logging
setup_logging()

print('Inicio lectura')

#envdir = '/home/ataverna/Documentos/proyectos/bao-madrid/den_files/'
#outdir = '/home/ataverna/Documentos/proyectos/bao-madrid/RascalC/output/nd3_00/'
envdir = '/home/ataverna/den_files/'
outdir = '/home/ataverna/RascalC/output/nd1_00/'

#env_list = ['nd0_00','nd0_96', 'nd1_00','nd1_22', 'nd2_00', 'nd3_00']
env = '1_00'

#rmin= 25.0; rmax= 150.0
#rmin= 70.0; rmax= 150.0
#rmin= 50.0; rmax= 170.0
rmin= 60.0; rmax= 160.0
#rmin= 30.0; rmax= 170.0
#rmin= 20.0; rmax= 200.0

rmins= str(int(rmin))
rmaxs= str(int(rmax))

if((rmin==25.) & (rmax==150.)):nbin=26
if((rmin==70.) & (rmax==150.)):nbin=17
#if((rmin==60.) & (rmax==160.)):nbin=21
if((rmin==60.) & (rmax==160.)):nbin=26 #binsize=4 Mpc/h
if((rmin==50.) & (rmax==170.)):nbin=25
if((rmin==30.) & (rmax==150.)):nbin=25
if((rmin==30.) & (rmax==170.)):nbin=29
if((rmin==20.) & (rmax==200.)):nbin=37

edges = np.linspace(rmin, rmax, nbin)

lbox = 1000.
boxsize = np.full(3, 1000.)
boxcenter = np.full(3, 500.)
redshift = 'z0'

ff = envdir+'mass_cuts_nd'+env+'_z0_fixedAmp_002.h5'
f = h5py.File(ff, 'r')
x = f['data/xgal'][:]
y = f['data/ygal'][:]
z = f['data/zgal'][:]
print(env,np.shape(x))
# Correct for periodic boundary effects
ind = np.where(x>=lbox) ; x[ind] = x[ind] - lbox
ind = np.where(y>=lbox) ; y[ind] = y[ind] - lbox
ind = np.where(z>=lbox) ; z[ind] = z[ind] - lbox
dat2 = np.column_stack([x]+[y]+[z])
print(ff)
print(env,np.shape(dat2))
f.close()
dat = dat2 #np.delete(dat2, np.where(dat2 >= 1000.0)[0], axis=0)
print(env,np.shape(dat))


tofile2 = []

#write 2pcf+error
outfil2 = outdir+'pycorr_z0_nd'+env+'_xi_r_'+rmins+'_'+rmaxs+'_4Mpc.dat'
with open(outfil2, 'w') as outf2:
    outf2.write('# xi: ndensity \n')


r = TwoPointCorrelationFunction('s', edges, data_positions1=dat,
        engine='corrfunc', boxsize=boxsize, nthreads='64',
        compute_sepsavg=False, position_type = 'pos')

rsep = r.sep
xi = r.corr
tofile2 = [rsep, xi]

#-------------------------------
# Write
#-------------------------------
with open(outfil2, 'a') as outf2:
    outf2.write('# xbin, xi_nd, err, err_poisson \n')
    np.savetxt(outf2,np.column_stack(tofile2),fmt=('%.20f'), delimiter="  ")
outf2.closed

print('Output: {}'.format(outfil2))