import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

##################################################
######################### l0 #####################

data = np.load('nd3_00/Rescaled_Covariance_Matrices_Legendre_n25_l0.npz') #nd3_00 fixedAmp_002
print(data.files)

cov=data.get('full_theory_covariance')
cov_i=data.get('individual_theory_covariances')

# the index of the position of yticks
num_ticks = 25
ticks = np.linspace(25, 145, num_ticks)

sns.heatmap(cov, cmap="crest", yticklabels=ticks, xticklabels=ticks)
plt.title('Covariance Matrix nd3_00')
plt.show()

nbin=25
R = np.zeros((nbin, nbin))
for i in range(0,nbin):
    for j in range(0,nbin):
        R[i,j] = cov[i,j]/np.sqrt(cov[i,i]*cov[j,j])

sns.heatmap(R, vmin=0, vmax=1, yticklabels=ticks, xticklabels=ticks)
plt.title(r'Normalised Covariance Matrix nd3_00: $C_{ij}$/$\sqrt{C_{ii}*C_{jj}}$')
plt.xlabel('r [Mpc/h]')
plt.ylabel('r [Mpc/h]')
plt.show()


# 25 bines entre r∈[25,150] sizebin=5 Mpc/h
error = np.diag(cov)**0.5

##################################################
##################################################
#calcuate 2pcr using pycorr
##################################################
dcorr=np.genfromtxt('nd3_00/pycorr_z0_nd3_00_xi_jkn_8_3_r_25_150.dat')

r = dcorr[:,0]
xi = dcorr[:,1]
err = dcorr[:,2]
errp = dcorr[:,3]


#plt.errorbar(r,r**2*xi,yerr=r**2*err,marker='.', label='pycorr nsv=8^3 (binsize=5 Mpc/h)')
plt.errorbar(r,r**2*xi,yerr=r**2*error, label='error RascalC')
#plt.errorbar(r,r**2*xi,yerr=r**2*errp, label='Poisson: (1 + ξ)/√(DD)',color='y')


dd=np.genfromtxt('nd3_00/xi_to_multipoles.dat')
r = dd[:,0]
xi = dd[:,1]
plt.plot(r,r**2*xi,color='red', linestyle='dotted', label='ξ0 RascalC (binsize=1 Mpc/h) nd3_00')


plt.legend()
plt.show()

stop

###################################
#nd1_00
###################################
data = np.load('nd1_00/Rescaled_Covariance_Matrices_Legendre_n25_l0.npz') #nd1_00 fixedAmp_002
print(data.files)
cov=data.get('full_theory_covariance')

# 25 bines entre r∈[25,150] sizebin=5 Mpc/h
error = np.diag(cov)**0.5

dcut=np.genfromtxt('nd1_00/pycorr_z0_nd3_00_xi_jkn_8_3_r_25_150.dat')
rc=dcut[:,0]
xic=dcut[:,1]

dd=np.genfromtxt('nd1_00/xi_to_multipoles.dat')
r = dd[:,0]
xi = dd[:,1]
plt.plot(r,r**2*xi,color='blue', linestyle='dotted', label='ξ0 RascalC (binsize=1 Mpc/h) nd1_00')
plt.plot(rc,rc**2*xic,color='red', linestyle='dotted', label='ξ0 RascalC (binsize=5 Mpc/h) nd1_00')
plt.errorbar(rc,rc**2*xic,yerr=rc**2*error,marker='.', label='RascalC error')

plt.legend()
plt.show()

###########################
## Legendre moment l0 y l2
###########################

data = np.load('nd3_00/Rescaled_Covariance_Matrices_Legendre_n25_l2.npz') #nd3_00 fixedAmp_002
print(data.files)

cov=data.get('full_theory_covariance')
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
