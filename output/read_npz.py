import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = np.load('Rescaled_Covariance_Matrices_Legendre_n25_l2.npz')
print(data.files)

cov=data.get('full_theory_covariance')
cov_i=data.get('individual_theory_covariances')

sns.heatmap(cov, cmap="crest")
plt.show()

nbin=50
R = np.zeros((nbin, nbin))
for i in range(0,nbin):
    for j in range(0,nbin):
        R[i,j] = cov[i,j]/np.sqrt(cov[i,i]*cov[j,j])

sns.heatmap(R, vmin=0, vmax=1)


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


sns.heatmap(cov_l2, vmin=0, vmax=1)

##################################################
######################### l0 #####################

data0 = np.load('Rescaled_Covariance_Matrices_Legendre_n25_l0.npz')
print(data0.files)

cov0=data0.get('full_theory_covariance')
cov0_i=data0.get('individual_theory_covariances')


sns.heatmap(cov0, cmap="crest")
plt.show()

nbin=25
R0 = np.zeros((nbin, nbin))
for i in range(0,nbin):
    for j in range(0,nbin):
        R0[i,j] = cov0[i,j]/np.sqrt(cov0[i,i]*cov0[j,j])

sns.heatmap(R0, vmin=0, vmax=1)
plt.show()







