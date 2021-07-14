#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 4, 2019

@author: pgoltstein
"""

#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# Imports

import numpy as np
import scipy.stats as scistats
import statsmodels.api as statsmodels


#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# Descriptives

def mean_sem( datamat, axis=0 ):
    mean = np.nanmean(datamat,axis=axis)
    n = np.sum( ~np.isnan( datamat ), axis=axis )
    sem = np.nanstd( datamat, axis=axis ) / np.sqrt( n )
    return mean,sem,n

def report_mean(sample1, sample2):
    print("  Group 1, Mean (SEM) = {} ({}) n={}".format(*mean_sem(sample1.ravel())))
    print("  Group 2, Mean (SEM) = {} ({}) n={}".format(*mean_sem(sample2.ravel())))

#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# Non-parametric testing

def report_wmpsr_test( sample1, sample2, n_indents=2, alpha=0.05, bonferroni=1, preceding_text=""):
    p,Z,n = wilcoxon_matched_pairs_signed_rank_test( sample1, sample2 )
    p_b = p*bonferroni
    print('{}{}WMPSR test, Z={:0.0f}, p={:4E}, p(b)={:4E}, n={:0.0f}{}'.format( " "*n_indents, preceding_text, Z, p, p_b, n, "  >> SIGN !!" if p<(alpha/bonferroni) else "." ))
    return p_b

def report_mannwhitneyu_test( sample1, sample2, n_indents=2, alpha=0.05, bonferroni=1 ):
    p,U,r,n1,n2 = mann_whitney_u_test( sample1, sample2 )
    p_b = p*bonferroni
    print('{}Mann-Whitney U test, U={:0.0f}, p={:4E}, p(b)={:4E}, r={:0.3f}, n1={:0.0f}, n2={:0.0f}{}'.format( " "*n_indents, U, p, p_b, r, n1, n2, "  >> SIGN !!" if p<(alpha/bonferroni) else "." ))
    return p_b

def report_kruskalwallis( samplelist, n_indents=2, alpha=0.05 ):
    p,H,DFbetween,DFwithin,n = kruskalwallis( samplelist )
    print("{}Kruskal-Wallis test, X^2 = {:0.3f}, df = {:0.0f} p = {}, n={:0.0f}".format( " "*n_indents, H, DFbetween, p, n, "  >> SIGN !!" if p<alpha else "." ))

def wilcoxon_matched_pairs_signed_rank_test( sample1, sample2 ):
    sample1 = sample1[~np.isnan(sample1)].ravel()
    sample2 = sample2[~np.isnan(sample2)].ravel()
    if np.count_nonzero(sample1)==0 and np.count_nonzero(sample2)==0:
        return 1.0,np.NaN,np.NaN
    else:
        Z,p = scistats.wilcoxon(sample1, sample2)
        n = len(sample1)
        return p,Z,n

def mann_whitney_u_test( sample1, sample2 ):
    sample1 = sample1[~np.isnan(sample1)].ravel()
    sample2 = sample2[~np.isnan(sample2)].ravel()
    U,p = scistats.mannwhitneyu(sample1, sample2)
    n1 = len(sample1)
    n2 = len(sample2)
    r = U / np.sqrt(n1+n2)
    return p,U,r,n1,n2

def kruskalwallis( samplelist ):
    # Clean up sample list and calculate N
    N = 0
    no_nan_samplelist = []
    for b in range(len(samplelist)):
        no_nan_samples = samplelist[b][~np.isnan(samplelist[b])]
        if len(no_nan_samples) > 0:
            no_nan_samplelist.append(no_nan_samples)
            N += len(no_nan_samples)

    # Calculate degrees of freedom
    k = len(samplelist)
    DFbetween = k - 1
    DFwithin = N - k
    DFtotal = N - 1
    H,p = scistats.kruskal( *no_nan_samplelist )
    return p,H,DFbetween,DFwithin,N
    
