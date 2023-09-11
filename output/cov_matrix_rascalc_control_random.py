import numpy as np

d1  = np.load('nd3_00/Rescaled_Covariance_Matrices_Legendre_n25_l0_1x.npz') #nd3_00 fixedAmp_002
d2  = np.load('nd3_00/Rescaled_Covariance_Matrices_Legendre_n25_l0_2x.npz') #nd3_00 fixedAmp_002
d5  = np.load('nd3_00/Rescaled_Covariance_Matrices_Legendre_n25_l0_5x.npz') #nd3_00 fixedAmp_002
d10 = np.load('nd3_00/Rescaled_Covariance_Matrices_Legendre_n25_l0_10x.npz') #nd3_00 fixedAmp_002
d1b= np.load('nd3_00/Rescaled_Covariance_Matrices_Legendre_n25_l0_60_160_1x.npz') #nd3_00 fixedAmp_002

print(d1.files)
cov1=d1.get('full_theory_covariance')
cov2=d2.get('full_theory_covariance')
cov5=d5.get('full_theory_covariance')
cov10=d10.get('full_theory_covariance')
cov1b=d1b.get('full_theory_covariance')


dcov10=np.diag(cov10)
dcov1=np.diag(cov1)
dcov2=np.diag(cov2)
dcov5=np.diag(cov5)

n10=np.sqrt(dcov10)
n1=np.sqrt(dcov1)
n2=np.sqrt(dcov2)
n5=np.sqrt(dcov5)

print('cov 10x/cov 1x',np.diag(cov10)/np.diag(cov1))
print('cov 5x/cov 1x',np.diag(cov5)/np.diag(cov1))
print('cov 2x/cov 1x',np.diag(cov2)/np.diag(cov1))
print('--------------------------------')
print('cov 10x/cov 1x',n10/n1)
print('cov 5x/cov 1x',n5/n1)
print('cov 2x/cov 1x',n2/n1)
print('--------------------------------')
#print('cov 10x/cov 1x',cov10/cov1)
#print('cov 5x/cov 1x',cov5/cov1)
#print('cov 2x/cov 1x',cov2/cov1)
print('--------------------------------')
#print('cov 1xb/cov 1x',np.sqrt(np.diag(cov1b))/n1)


p1=np.diag(d1.get('full_theory_precision'))
p2=np.diag(d2.get('full_theory_precision'))
np.sqrt(p1)/np.sqrt(p2)
