import numpy as np
from convert_cov import convert_cov

rand='1x'
#data = np.load('nd3_00/Rescaled_Covariance_Matrices_Legendre_n25_l0_'+rand+'.npz') #nd3_00 fixedAmp_002
data = np.load('nd3_00/Rescaled_Covariance_Matrices_Legendre_n25_l0_60_160_'+rand+'.npz') #nd3_00 fixedAmp_002
print(data.files)

cov=data.get('full_theory_covariance')

#rmin= 25.0; rmax= 150.0
rmin= 60.0; rmax= 160.0
rmins= str(int(rmin))
rmaxs= str(int(rmax))
env='3_00'

outdir = 'nd'+env+'/'
convert_cov(outdir+'cov_matrix_RascalC_z0_nd'+env+'_r_'+rmins+'_'+rmaxs+'_'+rand+'.bin',cov)


#-------------------------------
# Write
#-------------------------------
outfil = 'nd3_00/cov_matrix_RascalC_z0_nd'+env+'_r_'+rmins+'_'+rmaxs+'_'+rand+'.dat'
with open(outfil, 'a') as outf:
    outf.write('# nd cov matrix \n')
    np.savetxt(outf,np.column_stack(cov),fmt=('%.20f'), delimiter="  ")
outf.closed

print('Output: {}'.format(outfil))

