import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

##################################################
######################### l0 #####################
# r in [25-150]
# 25 bines entre r∈[25,150] sizebin=5 Mpc/h
#1x
data = np.load('nd3_00/Rescaled_Covariance_Matrices_Legendre_n25_l0_1x.npz') #nd3_00 fixedAmp_002
print(data.files)
cov=data.get('full_theory_covariance')
cov_i=data.get('individual_theory_covariances')
error = np.diag(cov)**0.5
#2x
data = np.load('nd3_00/Rescaled_Covariance_Matrices_Legendre_n25_l0_2x_bug.npz') #nd3_00 fixedAmp_002
cov2=data.get('full_theory_covariance')
err2x_bug= np.diag(cov2)**0.5
data = np.load('nd3_00/Rescaled_Covariance_Matrices_Legendre_n25_l0_2x.npz') #nd3_00 fixedAmp_002
cov2=data.get('full_theory_covariance')
err2x= np.diag(cov2)**0.5
#5x
data = np.load('nd3_00/Rescaled_Covariance_Matrices_Legendre_n25_l0_5x_bug.npz') #nd3_00 fixedAmp_002
cov5=data.get('full_theory_covariance')
err5x_bug= np.diag(cov5)**0.5
#10x
data = np.load('nd3_00/Rescaled_Covariance_Matrices_Legendre_n25_l0_10x_bug.npz') #nd3_00 fixedAmp_002
cov10=data.get('full_theory_covariance')
err10x_bug= np.diag(cov10)**0.5

cov_pycorr=np.genfromtxt('nd3_00/pycorr_z0_nd3_00_cov_jkn_8_3_r_25_150.dat')

# r in [60-160]
d2 = np.load('nd3_00/Rescaled_Covariance_Matrices_Legendre_n25_l0_60_160_1x.npz') #nd3_00 fixedAmp_002

cov2=d2.get('full_theory_covariance')
cov2_pycorr=np.genfromtxt('nd3_00/pycorr_z0_nd3_00_cov_jkn_8_3_r_60_160.dat')
# 25 bines entre r∈[60,160] sizebin=4 Mpc/h
error2 = np.diag(cov2)**0.5

################### plot ###################
fig, (ax1,ax2) = plt.subplots(1,2, figsize=(8,4))
#fig, ((ax1, ax2), (ax3, ax4))  = plt.subplots(2,2)

# the index of the position of yticks
num_ticks = 25
ticks = np.linspace(25, 145, num_ticks)

sns.heatmap(cov, cmap="crest", yticklabels=ticks, xticklabels=ticks,ax=ax1)
ax1.set_aspect(1)
ax1.set_title('RascalC')
sns.heatmap(cov_pycorr, cmap="crest", yticklabels=ticks, xticklabels=ticks,ax=ax2)
ax2.set_aspect(1)
ax2.set_title('Pycorr')

fig.suptitle('Covariance Matrix nd3_00')
plt.show()
##################################################

nbin=25
R = np.zeros((nbin, nbin))
R_pycorr = np.zeros((nbin, nbin))
for i in range(0,nbin):
    for j in range(0,nbin):
        R[i,j] = cov[i,j]/np.sqrt(cov[i,i]*cov[j,j])
        R_pycorr[i,j] = cov_pycorr[i,j]/np.sqrt(cov_pycorr[i,i]*cov_pycorr[j,j])


################### plot ###################
fig, (ax1,ax2) = plt.subplots(1,2, figsize=(12,5))
#fig.subplots_adjust(left=0.07, bottom=0.1, right=None, top=None, wspace=0.5, hspace=0.3)
#fig, ((ax1, ax2), (ax3, ax4))  = plt.subplots(2,2)

fig.suptitle(r'Normalised Covariance Matrix nd3_00: $C_{ij}$/$\sqrt{C_{ii}*C_{jj}}$')
# the index of the position of yticks
num_ticks = 25
ticks = np.linspace(25, 145, num_ticks)

sns.heatmap(R, vmin=0, vmax=1, cmap="coolwarm", yticklabels=ticks, xticklabels=ticks,ax=ax1)
ax1.set_aspect(1)
ax1.set_title('RascalC')
ax1.set_xlabel('r [Mpc/h]')
ax1.set_ylabel('r [Mpc/h]')
sns.heatmap(R_pycorr, vmin=0, vmax=1, cmap="coolwarm", yticklabels=ticks, xticklabels=ticks,ax=ax2)
ax2.set_aspect(1)
ax2.set_title('Pycorr')
plt.xlabel('r [Mpc/h]')
plt.ylabel('r [Mpc/h]')

plt.show()
##################################################



##################################################
#############################
#calcuate 2pcr using pycorr
#############################
dcorr=np.genfromtxt('nd3_00/pycorr_z0_nd3_00_xi_jkn_8_3_r_25_150.dat')

r = dcorr[:,0]
xi = dcorr[:,1]
err_pycorr = dcorr[:,2]
errp = dcorr[:,3]

dcorr2=np.genfromtxt('nd3_00/pycorr_z0_nd3_00_xi_jkn_8_3_r_60_160.dat')
rb = dcorr2[:,0]
xib = dcorr2[:,1]
errb_pycorr = dcorr2[:,2]

##############################
#calcuate 2pcf using fortran
##############################
#ff=np.genfromtxt('../../get_env/n_density/test_jackknife/fortran/output/xi_lin_nsv3_512_bao_nd3_00_rodajas.dat')
ff=np.genfromtxt('../../get_env/n_density/test_jackknife/fortran/output/xi_lin_nsv3_512_bao_nd3_00_subboxes.dat')

r_f = ff[:,0]-2.5
xi_f = ff[:,1]
err_f = ff[:,2]

################### plot ###################
#fig, (ax1,ax2) = plt.subplots(1,2, figsize=(12,5))
fig, ((ax1, ax2), (ax3, ax4))  = plt.subplots(2,2)
fig.subplots_adjust(left=0.07, bottom=0.1, right=None, top=None, wspace=0.5, hspace=0.3)

fig.suptitle(r'2pcf nd3_00')
# the index of the position of yticks
num_ticks = 25
ticks = np.linspace(25, 145, num_ticks)

ax1.errorbar(r,r**2*xi,yerr=r**2*error, label='error RascalC (binsize=5 Mpc/h)')
ax1.errorbar(r,r**2*xi,yerr=r**2*errp, marker='.', markersize=4, linestyle="None", label='Poisson: (1 + ξ)/√(DD)',color='y')
ax1.errorbar(rb,rb**2*xib,yerr=rb**2*error2, marker='.', markersize=4, linestyle="None", label='error RascalC (binsize=4 Mpc/h)',color='r')
#ax1.set_aspect(0.5)
ax1.set_ylim(-80,90)
ax1.set_xlabel('r [Mpc/h]')
ax1.set_ylabel(r'$r^2 \xi(r)$')
ax1.legend(fontsize=5)

ax2.errorbar(r,r**2*xi,yerr=r**2*err_pycorr, marker='.', label='pycorr nsv=8^3 (binsize=5 Mpc/h)')
#ax2.errorbar(r_f,r_f**2*xi_f,yerr=r_f**2*err_f, marker='.', label='fortran nsv=8^3 (binsize=5 Mpc/h)')
ax2.errorbar(r,r**2*xi,yerr=r**2*error, label='error RascalC (binsize=5 Mpc/h)')
#ax2.errorbar(rb,rb**2*xib,yerr=rb**2*errb, marker='.', markersize=4, linestyle="None", label='error RascalC (binsize=4 Mpc/h)',color='r')
#ax2.set_aspect(0.5)
ax2.set_ylim(-80,90)
ax2.set_xlabel('r [Mpc/h]')
ax2.set_ylabel(r'$r^2 \xi(r)$')
ax2.legend(fontsize=5)


ax3.errorbar(r,r**2*xi,yerr=r**2*err_pycorr, marker='.', label='pycorr nsv=8^3 (binsize=5 Mpc/h)')
ax3.errorbar(r,r**2*xi,yerr=r**2*err5x_bug, label='error RascalC 5x (c/bug)')
ax3.errorbar(r,r**2*xi,yerr=r**2*err2x_bug, label='error RascalC 2x (c/bug)')
ax3.errorbar(r,r**2*xi,yerr=r**2*error, label='error RascalC 1x (c/bug)')
#ax3.set_aspect(0.5)
ax3.set_ylim(-80,90)
ax3.set_xlabel('r [Mpc/h]')
ax3.set_ylabel(r'$r^2 \xi(r)$')
ax3.legend(fontsize=5)


ax4.errorbar(r,r**2*xi,yerr=r**2*err_pycorr, marker='.', label='pycorr nsv=8^3 (binsize=5 Mpc/h)')
#ax4.errorbar(r,r**2*xi,yerr=r**2*err10x, label='error RascalC 10x')
#ax4.errorbar(r,r**2*xi,yerr=r**2*err5x, label='error RascalC 5x')
ax4.errorbar(r,r**2*xi,yerr=r**2*err2x, label='error RascalC 2x')
ax4.errorbar(r,r**2*xi,yerr=r**2*error, label='error RascalC 1x')
#ax3.set_aspect(0.5)
ax4.set_ylim(-80,90)
ax4.set_xlabel('r [Mpc/h]')
ax4.set_ylabel(r'$r^2 \xi(r)$')
ax4.legend(fontsize=5)

plt.show()
##################################################
############################################
############# plot Misha ###################

fig, (ax3,ax4) = plt.subplots(1,2, figsize=(12,5))

fig.suptitle(r'2pcf nd3_00')
# the index of the position of yticks
num_ticks = 25
ticks = np.linspace(25, 145, num_ticks)

ax3.errorbar(r,r**2*xi,yerr=r**2*err5x_bug, label='error RascalC 5x (w/bug)',color='m')
ax3.errorbar(r,r**2*xi,yerr=r**2*err2x_bug, label='error RascalC 2x (w/bug)',color='g')
b=ax3.errorbar(r,r**2*xi,yerr=r**2*error, label='error RascalC 1x (w/bug)',color='r')
b[-1][0].set_linestyle('-.')
#ax3.set_aspect(0.5)
ax3.set_ylim(-80,90)
ax3.set_xlabel('r [Mpc/h]')
ax3.set_ylabel(r'$r^2 \xi(r)$')
ax3.legend(fontsize=10)

ax4.errorbar(r,r**2*xi,yerr=r**2*err_pycorr, marker='.', label='pycorr nsv=8^3 (binsize=5 Mpc/h)',color='b')
#ax4.errorbar(r,r**2*xi,yerr=r**2*err10x, label='error RascalC 10x')
#ax4.errorbar(r,r**2*xi,yerr=r**2*err5x, label='error RascalC 5x')
ax4.errorbar(r,r**2*xi,yerr=r**2*err2x, label='error RascalC 2x',color='g')
a=ax4.errorbar(r,r**2*xi,yerr=r**2*error, label='error RascalC 1x',color='r')
a[-1][0].set_linestyle('-.')
#ax3.set_aspect(0.5)
ax4.set_ylim(-80,90)
ax4.set_xlabel('r [Mpc/h]')
ax4.set_ylabel(r'$r^2 \xi(r)$')
ax4.legend(fontsize=10)

plt.show()
##################################################
##################################################
##################################################
##################################################

dd=np.genfromtxt('nd3_00/xi_to_multipoles.dat')
r = dd[:,0]
xi = dd[:,1]
#plt.plot(r,r**2*xi,color='red', linestyle='dotted', label='ξ0 RascalC (binsize=1 Mpc/h) nd3_00')
#plt.show()
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


stop
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



