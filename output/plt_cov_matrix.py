import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#data = np.load('Rescaled_Covariance_Matrices_Legendre_n25_l2.npz') #nd3_00 fixedAmp_001
data = np.load('nd3_00/Rescaled_Covariance_Matrices_Legendre_n25_l2.npz') #nd3_00 fixedAmp_002
print(data.files)

cov=data.get('full_theory_covariance')
cov_i=data.get('individual_theory_covariances')

sns.heatmap(cov, cmap="crest")
plt.show()

nbin=25
#nbin=50
R = np.zeros((nbin, nbin))
for i in range(0,nbin):
    for j in range(0,nbin):
        R[i,j] = cov[i,j]/np.sqrt(cov[i,i]*cov[j,j])

sns.heatmap(R, vmin=0, vmax=1)
plt.show()


nbin2=25
cov_l0 = np.zeros((nbin2, nbin2))
R_l0 = np.zeros((nbin2, nbin2))
cov_l2 = np.zeros((nbin2, nbin2))
R_l2 = np.zeros((nbin2, nbin2))

for i in range(0,nbin):
    for j in range(0,nbin):
        #l0
        if i%2==0:
            ii=int(i/2)
            if j%2==0:
                jj=int(j/2)
                cov_l0[ii,jj]=cov[i,j]
                R_l0[ii,jj] = cov[i,j]/np.sqrt(cov[i,i]*cov[j,j])
        #l2
        if i%2!=0:
            iii=int(i/2)
            if j%2!=0:
                jjj=int(j/2)
                cov_l2[iii,jjj]=cov[i,j]
                R_l2[iii,jjj] = cov[i,j]/np.sqrt(cov[i,i]*cov[j,j])


#sns.heatmap(cov_l2, vmin=0, vmax=1)
sns.heatmap(cov_l0)
plt.show()

sns.heatmap(R_l0, vmin=0, vmax=1.)
plt.show()

##################################################
######################### l0 #####################

data0 = np.load('Rescaled_Covariance_Matrices_Legendre_n25_l0.npz')
print(data0.files)

cov0=data0.get('full_theory_covariance')
cov0_i=data0.get('individual_theory_covariances')


sns.heatmap(cov0)
plt.show()

nbin=25
R0 = np.zeros((nbin, nbin))
for i in range(0,nbin):
    for j in range(0,nbin):
        R0[i,j] = cov0[i,j]/np.sqrt(cov0[i,i]*cov0[j,j])

sns.heatmap(R0, vmin=0, vmax=1)
plt.show()

# 25 bines entre r∈[25,150] sizebin=5 Mpc/h
error = np.diag(cov0)**0.5

##################################################
##################################################
#calcuate 2pcr using pycorr
##################################################

#d1=np.genfromtxt('../../get_env/n_density/test_jackknife/files/pycorr_z0_nd3_00_xi_jkn_8_3_r_25_150.dat')
dcorr=np.genfromtxt('nd3_00/pycorr_z0_nd3_00_xi_jkn_8_3_r_25_150.dat')

r = dcorr[:,0]
xi = dcorr[:,1]
err = dcorr[:,2]
err2 = np.diag(cov_l0)**0.5
errp = dcorr[:,3]

#plt.plot(err, err2)
#plt.show()

plt.errorbar(r,r**2*xi,yerr=r**2*err,marker='.', label='pycorr nsv=8^3 (binsize=5 Mpc/h)')
#plt.errorbar(r,r**2*xi,yerr=r**2*err2, label='error RascalC')
plt.errorbar(r,r**2*xi,yerr=r**2*errp, label='Poisson: (1 + ξ)/√(DD)',color='y')


dd=np.genfromtxt('nd3_00/xi_to_multipoles.dat')
r = dd[:,0]
xi = dd[:,1]
plt.plot(r,r**2*xi,color='red', linestyle='dotted', label='ξ0 RascalC (binsize=1 Mpc/h) nd3_00')


plt.legend()
plt.show()

#nd1_00
###################################
data = np.load('nd1_00/Rescaled_Covariance_Matrices_Legendre_n25_l0.npz') #nd1_00 fixedAmp_002
print(data.files)
cov=data.get('full_theory_covariance')

# 25 bines entre r∈[25,150] sizebin=5 Mpc/h
error = np.diag(cov)**0.5

dcut=np.genfromtxt('nd1_00/pru_plot.dat')
rc=dcut[:,0]
xic=dcut[:,1]

#d1=np.genfromtxt('../../get_env/n_density/test_jackknife/files/pycorr_z0_nd1_00_xi_jkn_8_3_r_60_160.dat')
dd=np.genfromtxt('nd1_00/xi_to_multipoles.dat')
r = dd[:,0]
xi = dd[:,1]
plt.plot(r,r**2*xi,color='blue', linestyle='dotted', label='ξ0 RascalC (binsize=1 Mpc/h) nd1_00')
plt.plot(rc,rc**2*xic,color='red', linestyle='dotted', label='ξ0 RascalC (binsize=5 Mpc/h) nd1_00')
plt.errorbar(rc,rc**2*xic,yerr=rc**2*error,marker='.', label='RascalC error')

plt.legend()
plt.show()
