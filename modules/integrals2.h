// Rewritten integrals.h code for grid_covariance.cpp (originally from Alex Wiegand) to parallelize and compute integrands to a given quad of particles
#include "parameters.h"
#include "correlation_function.h"
#include "cell_utilities.h"

#ifndef INTEGRALS_2_H
#define INTEGRALS_2_H

class Integrals2{
public:
    CorrelationFunction *cf;
    JK_weights *JK;
    
private:
    int nbin, mbin;
    Float rmin,rmax,mumin,mumax,dr,dmu; //Ranges in r and mu
    Float *Ra, *c2, *c3, *c4; // Arrays to accumulate integrals
    Float *cxj, *c2j, *c3j, *c4j; // Arrays to accumulate jackknife integrals
    Float *errc4, *errc4j, *errcxj; // Integral to house the variance in C4, C4j and Cxj;
    
    bool box,rad; // Flags to decide whether we have a periodic box and if we have a radial correlation function only
    
    uint64 *binct, *binct3, *binct4; // Arrays to accumulate bin counts
    
public:
    Integrals2(Parameters *par, CorrelationFunction *_cf, JK_weights *_JK){
        cf = new CorrelationFunction(_cf);
        JK = _JK;
        init(par);
    }
    
    void init(Parameters *par){
        nbin = par->nbin; // number of radial bins
        mbin = par->mbin; // number of mu bins
        
        int ec=0;
        // Initialize the binning
        ec+=posix_memalign((void **) &Ra, PAGE, sizeof(double)*nbin*mbin);
        ec+=posix_memalign((void **) &c2, PAGE, sizeof(double)*nbin*mbin);
        ec+=posix_memalign((void **) &c3, PAGE, sizeof(double)*nbin*mbin*nbin*mbin);
        ec+=posix_memalign((void **) &c4, PAGE, sizeof(double)*nbin*mbin*nbin*mbin);
        
        ec+=posix_memalign((void **) &c2j, PAGE, sizeof(double)*nbin*mbin);
        ec+=posix_memalign((void **) &c3j, PAGE, sizeof(double)*nbin*mbin*nbin*mbin);
        ec+=posix_memalign((void **) &c4j, PAGE, sizeof(double)*nbin*mbin*nbin*mbin);
        ec+=posix_memalign((void **) &cxj, PAGE, sizeof(double)*nbin*mbin*nbin*mbin);
        
        ec+=posix_memalign((void **) &errc4, PAGE, sizeof(double)*nbin*mbin*nbin*mbin);
        ec+=posix_memalign((void **) &errc4j, PAGE, sizeof(double)*nbin*mbin*nbin*mbin);
        ec+=posix_memalign((void **) &errcxj, PAGE, sizeof(double)*nbin*mbin*nbin*mbin);
        
        ec+=posix_memalign((void **) &binct, PAGE, sizeof(uint64)*nbin*mbin);
        ec+=posix_memalign((void **) &binct3, PAGE, sizeof(uint64)*nbin*mbin*nbin*mbin);
        ec+=posix_memalign((void **) &binct4, PAGE, sizeof(uint64)*nbin*mbin*nbin*mbin);

        assert(ec==0);

        reset();

        box=par->perbox;

        rmax=par->rmax;
        rmin=par->rmin;

        mumax=par->mumax;
        mumin=par->mumin;

        dr=(rmax-rmin)/nbin;
        dmu=(mumax-mumin)/mbin;

        rad=mbin==1&&dmu==1.;

    }

    ~Integrals2() {
        free(Ra);
        free(c2);
        free(c3);
        free(c4);
        free(cxj);
        free(c2j);
        free(c3j);
        free(c4j);
        free(errc4);
        free(errc4j);
        free(errcxj);
        free(binct);
        free(binct3);
        free(binct4);

    }

    void reset(){
        for (int j=0; j<nbin*mbin; j++) {
            Ra[j] = 0;
            c2[j] = 0;
            c2j[j] = 0;
            binct[j] = 0;
        }
        for (int j=0; j<nbin*mbin*nbin*mbin; j++) {
            c3[j]=0;
            c4[j]=0;
            c3j[j]=0;
            c4j[j]=0;
            cxj[j] = 0;
            errc4[j] = 0;
            errc4j[j] = 0;
            errcxj[j] = 0;
            binct3[j] = 0;
            binct4[j] = 0;
        }
    }

    inline int getbin(Float r, Float mu){
        // Linearizes 2D indices
        return floor((r-rmin)/dr) *mbin + floor((mu-mumin)/dmu);
    }
    
    inline void second(const Particle* pi_list, const int* prim_ids, int pln, const Particle pj, const int pj_id, Float* &xi_ij, int* &bin, Float* &wij, const double prob){
        // Accumulates the two point integral C2. Also outputs an array of xi_ij and bin values for later reuse.
        // Prob. here is defined as g_ij / f_ij where g_ij is the sampling PDF and f_ij is the true data PDF for picking pairs (equal to n_i/N n_j/N for N particles)
        
        for(int i=0;i<pln;i++){ // Iterate over particle in pi_list
                Float rij_mag,rij_mu, rav, c2v, c2vj;
                Particle pi = pi_list[i]; // first particle
                
                if(prim_ids[i]==pj_id){
                    wij[i]=-1;
                    continue; // don't self-count
                }
                
                cleanup_l(pi.pos,pj.pos,rij_mag,rij_mu); // define |r_ij| and ang(r_ij)
                int tmp_bin = getbin(rij_mag, rij_mu); // bin for each particle
                
                if ((tmp_bin<0)||(tmp_bin>=nbin*mbin)){
                    wij[i]=-1;
                    continue; // if not in correct bin
                }
                
                Float tmp_weight = pi.w*pj.w; // product of weights
                Float tmp_xi = cf->xi(rij_mag, rij_mu); // correlation function for i-j
                
                // Save into arrays for later
                bin[i]=tmp_bin;
                xi_ij[i] = tmp_xi;
                wij[i] = tmp_weight;
                
                 // Compute jackknife weight tensor:
                Float JK_weight;
                JK_weight=weight_tensor(int(pi.JK),int(pj.JK),int(pi.JK),int(pj.JK),tmp_bin,tmp_bin);
            
                // Now compute the integral:
                c2vj = 2.*tmp_weight*tmp_weight*(1.+tmp_xi)/prob*JK_weight;
                c2v = 2.*tmp_weight*tmp_weight*(1.+tmp_xi) / prob; // c2 contribution
                rav = tmp_weight / prob; // RR_a contribution
                
                // Add to local integral counts:
                Ra[tmp_bin]+=rav;
                c2[tmp_bin]+=c2v;
                c2j[tmp_bin]+=c2vj;
                binct[tmp_bin]++; // only count actual contributions to bin
        }
    }
    
    inline void third(const Particle* pi_list, const int* prim_ids, const int pln, const Particle pj, const Particle pk, const int pj_id, const int pk_id, const int* bin_ij, const Float* wij, Float* &xi_jk, Float* &xi_ik, Float* wijk, const double prob){
        // Accumulates the three point integral C3. Also outputs an array of xi_ik and bin_ik values for later reuse.
        
        for(int i=0;i<pln;i++){ // Iterate ovr particle in pi_list
            Particle pi = pi_list[i];
            Float rik_mag,rik_mu,c3v,c3vj,rjk_mag, rjk_mu;
            if(wij[i]==-1){
                wijk[i]=-1;
                continue; // skip incorrect bins / ij self counts
            }
            
            if((prim_ids[i]==pk_id)||(pk_id==pj_id)){
                wijk[i]=-1; // re-read to skip this later
                continue; // don't self-count
            }
            
            cleanup_l(pi.pos,pk.pos,rik_mag,rik_mu); // define angles/lengths
            
            int tmp_bin = getbin(rik_mag,rik_mu); // bin for each particle
            
            if ((tmp_bin<0)||(tmp_bin>=nbin*mbin)){
                wijk[i] = -1;
                continue; // if not in correct bin
            }
            
            cleanup_l(pj.pos,pk.pos,rjk_mag,rjk_mu); 
            
            Float tmp_weight = wij[i]*pk.w; // product of weights, w_iw_jw_k
            Float xi_jk_tmp = cf->xi(rjk_mag, rjk_mu); // correlation function for j-k
            Float xi_ik_tmp = cf->xi(rik_mag, rik_mu); // not used here but used later
            
            // save arrays for later
            xi_jk[i]=xi_jk_tmp;
            xi_ik[i]=xi_ik_tmp;
            wijk[i]=tmp_weight;
            
            // Compute jackknife weight tensor:
            Float JK_weight;
            JK_weight=weight_tensor(int(pi.JK),int(pj.JK),int(pk.JK),int(pi.JK),bin_ij[i],tmp_bin);
            
            // Now compute the integral (using symmetry factor of 4);
            c3v = 4.*tmp_weight*pi.w/prob*xi_jk_tmp;
            c3vj = 4.*tmp_weight*pi.w/prob*xi_jk_tmp*JK_weight;
            
            // Add to local counts
            int tmp_full_bin = bin_ij[i]*mbin*nbin+tmp_bin;
            c3[tmp_full_bin]+=c3v;
            c3j[tmp_full_bin]+=c3vj;
            binct3[tmp_full_bin]++;
        }
    }
        
    inline void fourth(const Particle* pi_list, const int* prim_ids, const int pln, const Particle pj, const Particle pk, const Particle pl, const int pj_id, const int pk_id, const int pl_id, const int* bin_ij, const Float* wijk, const Float* xi_ik, const Float* xi_jk, const Float* xi_ij, const double prob){
        // Accumulates the three point integral C3. Also outputs an array of xi_ik and bin_ik values for later reuse.
        
        for(int i=0;i<pln;i++){ // Iterate over particle in pi_list
            Particle pi = pi_list[i];
            Float ril_mag,ril_mu,rjl_mag, rjl_mu, rkl_mag, rkl_mu, c4v, c4vj, cxvj;
            if(wijk[i]==-1) continue; // skip incorrect bins / ij self counts
            
            if((prim_ids[i]==pl_id)||(pj_id==pl_id)||(pk_id==pl_id)) continue; // don't self-count
            
            cleanup_l(pk.pos, pl.pos, rkl_mag, rkl_mu); // define angles/lengths
            int tmp_bin = getbin(rkl_mag,rkl_mu); // kl bin for each particle
            
            if ((tmp_bin<0)||(tmp_bin>=nbin*mbin)) continue; // if not in correct bin
            
            cleanup_l(pl.pos,pi.pos,ril_mag,ril_mu); 
            cleanup_l(pl.pos,pj.pos,rjl_mag,rjl_mu); 
            
            Float tmp_weight = wijk[i]*pl.w; // product of weights, w_i*w_j*w_k*w_l
            Float xi_il = cf->xi(ril_mag, ril_mu); // correlation function for i-l
            Float xi_jl = cf->xi(rjl_mag, rjl_mu); // j-l correlation
            Float xi_kl = cf->xi(rkl_mag, rkl_mu); // k-l correlation
            
            // Compute jackknife weight tensor:
            Float JK_weight;
            JK_weight=weight_tensor(int(pi.JK),int(pj.JK),int(pk.JK),int(pl.JK),bin_ij[i],tmp_bin);
            
            // Now compute the integral;
            c4v = tmp_weight/prob*(xi_il*xi_jk[i]+xi_jl*xi_ik[i]);
            c4vj = tmp_weight/prob*(xi_il*xi_jk[i]+xi_jl*xi_ik[i])*JK_weight;
            cxvj = tmp_weight/prob*(xi_ij[i]*xi_kl)*JK_weight;
            
            // Add to local counts
            int tmp_full_bin = bin_ij[i]*mbin*nbin+tmp_bin;
            c4[tmp_full_bin]+=c4v;
            c4j[tmp_full_bin]+=c4vj;
            cxj[tmp_full_bin]+=cxvj;
            errc4[tmp_full_bin]+=pow(c4v,2.);
            errc4j[tmp_full_bin]+=pow(c4vj,2.);
            errcxj[tmp_full_bin]+=pow(cxvj,2.);
            binct4[tmp_full_bin]++;            
        }
    }
        
private:   
    inline Float weight_tensor(const int Ji, const int Jj, const int Jk, const int Jl, const int bin_a, const int bin_b){
        // Compute the jackknife weight tensor for jackknife regions J_i, J_j, J_k, J_l and w_aA weight matrix w_matrix. NB: J_x are collapsed jackknife indices here - only using the non-empty regions.
        // JK_weights class holds list of filled JKs, number of filled JKs and the weight matrix.
        // bin_a, bin_b specify the binning.
        
        int nbins = JK->nbins;
        
        // Compute q_ij^A q_kl^A term
        int first_weight = 0;
        if (Ji==Jk) first_weight++;
        if (Jj==Jk) first_weight++;
        if (Ji==Jl) first_weight++;
        if (Jj==Jl) first_weight++;
        
        // Compute q_ijw_bA _ q_klw_aA part
        Float second_weight=JK->weights[Ji*nbins+bin_b]+JK->weights[Jj*nbins+bin_b]+JK->weights[Jk*nbins+bin_a]+JK->weights[Jl*nbins+bin_a];
        
        // Compute total weight (third part is precomputed)
        Float total_weight = (Float)first_weight/4. - 0.5*second_weight + JK->product_weights[bin_a*nbins+bin_b];
        
        return total_weight;
        
    }
        
    void cleanup_l(Float3 p1,Float3 p2,Float& norm,Float& mu){
        Float3 pos=p1-p2;
        norm = pos.norm();
        // If the input correlation function had only radial information and no mu bins
        // fill the dummy mu bins by 0.5
        if(rad){
            mu=0.5;
        }
        else{
#ifndef PERIODIC
            Float3 los=p1+p2; // No 1/2 as normalized anyway below
            mu = fabs(pos.dot(los)/norm/los.norm());
#else
            // In the periodic case use z-direction for mu
            mu = fabs(pos.z/norm);
#endif
        }
    }
public:
    void sum_ints(Integrals2* ints) {
        // Add the values accumulated in ints to the corresponding internal sums
        for(int i=0;i<nbin*mbin;i++){
            Ra[i]+=ints->Ra[i];
            c2[i]+=ints->c2[i];
            c2j[i]+=ints->c2j[i];
            binct[i]+=ints->binct[i];
        }
        for(int i=0;i<nbin*mbin;i++){
            for(int j=0;j<nbin*mbin;j++){
                c3[i*nbin*mbin+j]+=ints->c3[i*nbin*mbin+j];
                c3j[i*nbin*mbin+j]+=ints->c3j[i*nbin*mbin+j];
                c4[i*nbin*mbin+j]+=ints->c4[i*nbin*mbin+j];
                c4j[i*nbin*mbin+j]+=ints->c4j[i*nbin*mbin+j];
                cxj[i*nbin*mbin+j]+=ints->cxj[i*nbin*mbin+j];
                errc4[i*nbin*mbin+j]+=ints->errc4[i*nbin*mbin+j];
                errc4j[i*nbin*mbin+j]+=ints->errc4j[i*nbin*mbin+j];
                errcxj[i*nbin*mbin+j]+=ints->errcxj[i*nbin*mbin+j];
                binct3[i*nbin*mbin+j]+=ints->binct3[i*nbin*mbin+j];
                binct4[i*nbin*mbin+j]+=ints->binct4[i*nbin*mbin+j];
            }
        }
    }
    
    void frobenius_difference_sum(Integrals2* ints, int n_loop, Float &frobC2, Float &frobC3, Float &frobC4, Float &frobC2j, Float &frobC3j, Float &frobC4j, Float &frobCxj, Float &ratio_x4){
        // Add the values accumulated in ints to the corresponding internal sums and compute the Frobenius norm difference between integrals
        Float n_loops = (Float)n_loop;
        Float self_c2=0, diff_c2=0;
        Float self_c3=0, diff_c3=0;
        Float self_c4=0, diff_c4=0;
        Float self_c2j=0, diff_c2j=0;
        Float self_c3j=0, diff_c3j=0;
        Float self_c4j=0, diff_c4j=0;
        Float self_cxj=0, diff_cxj=0;
        
        // Compute Frobenius norms
        for(int i=0;i<nbin*mbin;i++){
            self_c2+=pow(c2[i]/n_loops,2.);
            diff_c2+=pow(c2[i]/n_loops-(c2[i]+ints->c2[i])/(n_loops+1.),2.);
            self_c2j+=pow(c2j[i]/n_loops,2.);
            diff_c2j+=pow(c2j[i]/n_loops-(c2j[i]+ints->c2j[i])/(n_loops+1.),2.);
            
            for(int j=0;j<nbin*mbin;j++){
                self_c4+=pow(c4[i*nbin*mbin+j]/n_loops,2.);
                diff_c4+=pow(c4[i*nbin*mbin+j]/n_loops-(c4[i*nbin*mbin+j]+ints->c4[i*nbin*mbin+j])/(n_loops+1.),2.);
                self_c4j+=pow(c4j[i*nbin*mbin+j]/n_loops,2.);
                diff_c4j+=pow(c4j[i*nbin*mbin+j]/n_loops-(c4j[i*nbin*mbin+j]+ints->c4j[i*nbin*mbin+j])/(n_loops+1.),2.);
                self_cxj+=pow(cxj[i*nbin*mbin+j]/n_loops,2.);
                diff_cxj+=pow(cxj[i*nbin*mbin+j]/n_loops-(cxj[i*nbin*mbin+j]+ints->cxj[i*nbin*mbin+j])/(n_loops+1.),2.);
                self_c3+=pow(c3[i*nbin*mbin+j]/n_loops,2.);
                diff_c3+=pow(c3[i*nbin*mbin+j]/n_loops-(c3[i*nbin*mbin+j]+ints->c3[i*nbin*mbin+j])/(n_loops+1.),2.);
                self_c3j+=pow(c3j[i*nbin*mbin+j]/n_loops,2.);
                diff_c3j+=pow(c3j[i*nbin*mbin+j]/n_loops-(c3j[i*nbin*mbin+j]+ints->c3j[i*nbin*mbin+j])/(n_loops+1.),2.);
                c3[i*nbin*mbin+j]+=ints->c3[i*nbin*mbin+j];
                c4[i*nbin*mbin+j]+=ints->c4[i*nbin*mbin+j];
                c3j[i*nbin*mbin+j]+=ints->c3j[i*nbin*mbin+j];
                c4j[i*nbin*mbin+j]+=ints->c4j[i*nbin*mbin+j];
                cxj[i*nbin*mbin+j]+=ints->cxj[i*nbin*mbin+j];
                binct3[i*nbin*mbin+j]+=ints->binct3[i*nbin*mbin+j];
                binct4[i*nbin*mbin+j]+=ints->binct4[i*nbin*mbin+j];
            }
            c2[i]+=ints->c2[i];
            c2j[i]+=ints->c2j[i];
            binct[i]+=ints->binct[i];
        }
        
        // Now update Ra values
        for(int i=0;i<nbin*mbin;i++){
            Ra[i]+=ints->Ra[i];
        }
        
        self_c2=sqrt(self_c2);
        diff_c2=sqrt(diff_c2);
        diff_c3=sqrt(diff_c3);
        diff_c4=sqrt(diff_c4);
        self_c3=sqrt(self_c3);
        self_c4=sqrt(self_c4);
        
        
        self_c2j=sqrt(self_c2j);
        diff_c2j=sqrt(diff_c2j);
        diff_c3j=sqrt(diff_c3j);
        diff_c4j=sqrt(diff_c4j);
        diff_cxj=sqrt(diff_cxj);
        self_c3j=sqrt(self_c3j);
        self_c4j=sqrt(self_c4j);
        self_cxj=sqrt(self_cxj);
        
        // Return percent difference
        frobC2=100.*(diff_c2/self_c2);
        frobC3=100.*(diff_c3/self_c3);
        frobC4=100.*(diff_c4/self_c4);
        frobC2j=100.*(diff_c2j/self_c2j);
        frobC3j=100.*(diff_c3j/self_c3j);
        frobC4j=100.*(diff_c4j/self_c4j);
        frobCxj=100.*(diff_cxj/self_cxj);
        
        ratio_x4 = self_cxj/self_c4j;
    }

    void sum_total_counts(uint64& acc2, uint64& acc3, uint64& acc4){
        // Add local counts to total bin counts in acc2-4
        for (int i=0; i<nbin*mbin; i++) {
            acc2+=binct[i];
            for (int j=0; j<nbin*mbin; j++) {
                acc3+=binct3[i*nbin*mbin+j];
                acc4+=binct4[i*nbin*mbin+j];
            }
        }
    }
    
    void normalize(int np, int ngal, Float n_pairs, Float n_triples, Float n_quads, bool use_RR){
        // Normalize the accumulated integrals (partly done by the normalising probabilities used from the selected cubes)
        // np is the number of random particles used, ngal is the number of galaxies in the survey
        // n_pair etc. are the number of PARTICLE pairs etc. attempted (not including rejected cells, but including pairs which don't fall in correct bin ranges)
        // If use_RR=True, we normalize by RR_a, RR_b also
        double corrf = (double)np/ngal; // Correction factor for the different densities of random points
        // To avoid recomputation
        double corrf2 = pow(corrf,2.);
        double corrf3 = corrf2*corrf;
        double corrf4 = corrf3*corrf;
        double corrf8 = corrf4*corrf4;
        
        for(int i = 0; i<nbin*mbin;i++){
            Ra[i]/=(n_pairs*corrf2);
            c2[i]/=(n_pairs*corrf2);
            c2j[i]/=(n_pairs*corrf2);
            for(int j=0;j<nbin*mbin;j++){
                c3[i*nbin*mbin+j]/=(n_triples*corrf3);
                c4[i*nbin*mbin+j]/=(n_quads*corrf4);
                c3j[i*nbin*mbin+j]/=(n_triples*corrf3);
                c4j[i*nbin*mbin+j]/=(n_quads*corrf4);
                cxj[i*nbin*mbin+j]/=(n_quads*corrf4);
                errc4[i*nbin*mbin+j]/=(n_quads*corrf8);
                errc4j[i*nbin*mbin+j]/=(n_quads*corrf8);
                errcxj[i*nbin*mbin+j]/=(n_quads*corrf8);
            }
        }
        
        
        if(use_RR==1){
            // Further normalize by RR counts
            //NEW: Normalizing by RR counts from corrfunc:
            for(int i=0; i<nbin*mbin;i++){
                Float Ra_i = JK->RR_pair_counts[i]; 
                c2[i]/=pow(Ra_i,2.); // must normalize by galaxy number here
                c2j[i]/=pow(Ra_i,2.)*(1.-JK->product_weights[i*nbin*mbin+i]);
                for(int j=0;j<nbin*mbin;j++){
                    Float Rab=Ra_i*JK->RR_pair_counts[j];
                    Float Rab_jk = Rab*(1.-JK->product_weights[i*nbin*mbin+j]);
                    c3[i*nbin*mbin+j]/=Rab;
                    c4[i*nbin*mbin+j]/=Rab;
                    c3j[i*nbin*mbin+j]/=Rab_jk;
                    c4j[i*nbin*mbin+j]/=Rab_jk;
                    cxj[i*nbin*mbin+j]/=Rab_jk;
                    errc4[i*nbin*mbin+j]/=pow(Rab_jk,2.);
                    errc4j[i*nbin*mbin+j]/=pow(Rab_jk,2.);
                    errcxj[i*nbin*mbin+j]/=pow(Rab_jk,2.);
                }
            }
        }
    }
        
    
    void save_integrals(char* suffix) {
    /* Print integral outputs to file. 
        * In txt files {c2,c3,c4,RR}_n{nbin}_m{mbin}.txt there are lists of the outputs of c2,c3,c4 and RR_a that are already normalized and multiplied by combinatoric factors. The n and m strings specify the number of n and m bins present.
        */
        // Create output files
        
        //TODO: Remove
        // ALSO SAVE BIN COUNTS:
        char binname[1000];
        snprintf(binname,sizeof binname, "CovMatricesAll/binct_c4_n%d_m%d_%s.txt",nbin,mbin,suffix);
        FILE * BinFile = fopen(binname,"w");
        
        char c2name[1000];
        snprintf(c2name, sizeof c2name, "CovMatricesAll/c2_n%d_m%d_%s.txt", nbin, mbin,suffix);
        char c3name[1000];
        snprintf(c3name, sizeof c3name, "CovMatricesAll/c3_n%d_m%d_%s.txt", nbin, mbin, suffix);
        char c4name[1000];
        snprintf(c4name, sizeof c4name, "CovMatricesAll/c4_n%d_m%d_%s.txt", nbin, mbin, suffix);
        char c4errname[1000];
        snprintf(c4errname, sizeof c4errname, "CovMatricesAll/c4err_n%d_m%d_%s.txt", nbin, mbin, suffix);
        char RRname[1000];
        snprintf(RRname, sizeof RRname, "CovMatricesAll/RR_n%d_m%d_%s.txt", nbin, mbin, suffix);
        FILE * C2File = fopen(c2name,"w"); // for c2 part of integral
        FILE * C3File = fopen(c3name,"w"); // for c3 part of integral
        FILE * C4File = fopen(c4name,"w"); // for c4 part of integral
        FILE * C4ErrFile = fopen(c4errname,"w"); // for variance of c4 part
        FILE * RRFile = fopen(RRname,"w"); // for RR part of integral
        
        for (int j=0;j<nbin*mbin;j++){
            fprintf(C2File,"%le\n",c2[j]);
            fprintf(RRFile,"%le\n",Ra[j]);
        }
        for(int i=0;i<nbin*mbin;i++){
            for(int j=0;j<nbin*mbin;j++){
                //TODO: Remove bin
                fprintf(BinFile,"%llu\t",binct4[i*nbin*mbin+j]);
                fprintf(C3File,"%le\t",c3[i*nbin*mbin+j]);
                fprintf(C4File,"%le\t",c4[i*nbin*mbin+j]);
                fprintf(C4ErrFile,"%le\t",errc4[i*nbin*mbin+j]);
            }
            fprintf(BinFile,"\n");
            fprintf(C3File,"\n"); // new line each end of row
            fprintf(C4File,"\n");
            fprintf(C4ErrFile,"\n");
        }
        fflush(NULL);
        
        // Close open files
        
        fclose(C2File);
        fclose(C3File);
        fclose(C4File);
        fclose(C4ErrFile);
        fclose(RRFile);
                    
    }

    
    void save_jackknife_integrals(char* suffix) {
    /* Print jackknife integral outputs to file. 
        * In txt files {c2,c3,c4,RR}_n{nbin}_m{mbin}.txt there are lists of the outputs of c2,c3,c4 and RR_a that are already normalized and multiplied by combinatoric factors. The n and m strings specify the number of n and m bins present.
        */
        // Create output files
        char c2name[1000];
        snprintf(c2name, sizeof c2name, "CovMatricesJack/c2j_n%d_m%d_%s.txt", nbin, mbin,suffix);
        char c3name[1000];
        snprintf(c3name, sizeof c3name, "CovMatricesJack/c3j_n%d_m%d_%s.txt", nbin, mbin, suffix);
        char c4name[1000];
        snprintf(c4name, sizeof c4name, "CovMatricesJack/c4j_n%d_m%d_%s.txt", nbin, mbin, suffix);
        char cxname[1000];
        snprintf(cxname, sizeof cxname, "CovMatricesJack/cxj_n%d_m%d_%s.txt", nbin, mbin, suffix);
        char c4errname[1000];
        snprintf(c4errname, sizeof c4errname, "CovMatricesJack/c4errj_n%d_m%d_%s.txt", nbin, mbin, suffix);
        char cxerrname[1000];
        snprintf(cxerrname, sizeof cxerrname, "CovMatricesJack/cxerrj_n%d_m%d_%s.txt", nbin, mbin, suffix);
        FILE * C2File = fopen(c2name,"w"); // for c2 part of integral
        FILE * C3File = fopen(c3name,"w"); // for c3 part of integral
        FILE * C4File = fopen(c4name,"w"); // for c4 part of integral
        FILE * CXFile = fopen(cxname,"w"); // for RR part of integral
        FILE * C4ErrFile = fopen(c4errname,"w"); // for c4 part of integral
        FILE * CXErrFile = fopen(cxerrname,"w"); // for c4 part of integral
        
        for (int j=0;j<nbin*mbin;j++){
            fprintf(C2File,"%le\n",c2j[j]);
        }
        for(int i=0;i<nbin*mbin;i++){
            for(int j=0;j<nbin*mbin;j++){
                fprintf(C3File,"%le\t",c3j[i*nbin*mbin+j]);
                fprintf(C4File,"%le\t",c4j[i*nbin*mbin+j]);
                fprintf(CXFile,"%le\t",cxj[i*nbin*mbin+j]);
                fprintf(C4ErrFile,"%le\t",errc4j[i*nbin*mbin+j]);
                fprintf(CXErrFile,"%le\t",errcxj[i*nbin*mbin+j]);
            }
            fprintf(C3File,"\n"); // new line each end of row
            fprintf(C4File,"\n");
            fprintf(CXFile,"\n");
            fprintf(C4ErrFile,"\n");
            fprintf(CXErrFile,"\n");
        }
        fflush(NULL);
        
        // Close open files
        
        fclose(C2File);
        fclose(C3File);
        fclose(C4File);
        fclose(CXFile);
        fclose(C4ErrFile);
        fclose(CXErrFile);
                    
    }
    
    void compute_Neff(Float n_quads, Float &N_eff, Float &N_eff_jack, Float &N_eff_x){
        // Compute the effective mean N from the data given the number of sets of quads used. 
        // This takes unnormalized integrals as inputs
        Float N4=0., N4j=0., N4x=0.;
        Float norm4=0., norm4j=0., normxj=0.;
        
        for(int i=0;i<nbin*mbin;i++){
            for(int j=0;j<nbin*mbin;j++){
                // Read in integral components + normalize by 1/n_quads;
                Float c4ij=c4[i*nbin*mbin+j]/n_quads;
                Float c4ii=c4[i*nbin*mbin+i]/n_quads;
                Float c4jj=c4[j*nbin*mbin+j]/n_quads;
                
                Float c4j_ij=c4j[i*nbin*mbin+j]/n_quads;
                Float c4j_ii=c4j[i*nbin*mbin+i]/n_quads;
                Float c4j_jj=c4j[j*nbin*mbin+j]/n_quads;
                
                Float cxj_ij=cxj[i*nbin*mbin+j]/n_quads;
                Float cxj_ii=cxj[i*nbin*mbin+i]/n_quads;
                Float cxj_jj=cxj[j*nbin*mbin+j]/n_quads;
                
                // Compute pixel variances
                Float var_c4 = (errc4[i*nbin*mbin+j]/n_quads - pow(c4ij,2.))/(n_quads-1.);
                Float var_c4j = (errc4j[i*nbin*mbin+j]/n_quads - pow(c4j_ij,2.))/(n_quads-1.);
                Float var_cxj = (errcxj[i*nbin*mbin+j]/n_quads - pow(cxj_ij,2.))/(n_quads-1.);
                
                // For N4;
                N4+=(pow(c4ij,2.)+c4ii*c4jj)/var_c4*c4ij;//*pow(c4ij,2.)
                norm4+=c4ij;//pow(c4ij,2.);
                
                // For N4j;
                N4j+=(pow(c4j_ij,2.)+c4j_ii*c4j_jj)/var_c4j*c4j_ij;//*pow(cjtot_tmp_ij,2.)
                norm4j+=c4j_ij;//pow(cjtot_tmp_ij,2.);
                
                // For N4x;
                N4x+=(pow(cxj_ij,2.)+cxj_ii*cxj_jj)/var_cxj*cxj_ij;
                normxj+=cxj_ij;
            }
        }
        N_eff = N4/norm4;
        N_eff_jack=N4j/norm4j;
        N_eff_x = N4x/normxj;
    }

};

#endif