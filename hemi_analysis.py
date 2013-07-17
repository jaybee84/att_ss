import numpy as np
import scipy.optimize as opt
from scipy.special import erf
import matplotlib.pyplot as plt

import tools


def cumgauss(x, mu, sigma):
    """
    The cumulative Gaussian at x, for the distribution with mean mu and
    standard deviation sigma. 

    Parameters
    ----------
    x : float or array
       The values of x over which to evaluate the cumulative Gaussian function

    mu : float 
       The mean parameter. Determines the x value at which the y value is 0.5
   
    sigma : float 
       The variance parameter. Determines the slope of the curve at the point of 
       Deflection
    
    Returns
    -------

    Notes
    -----
    Based on:
    http://en.wikipedia.org/wiki/Normal_distribution#Cumulative_distribution_function

    """
    return 0.5 * (1 + erf((x-mu)/(np.sqrt(2)*sigma)))


def err_func(params, x, y, func):
        """
        Error function for fitting a function
        
        Parameters
        ----------
        params : tuple
            A tuple with the parameters of `func` according to their order of
            input

        x : float array 
            An independent variable. 
        
        y : float array
            The dependent variable. 
        
        func : function
            A function with inputs: `(x, *params)`
        
        Returns
        -------
        The marginals of the fit to x/y given the params
        """
        return y - func(x, *params)

def analyze(f_name, fig_name=None, boot=1000):
    """
    """
    params_out = []
    
    p, l, data_rec = tools.get_data(f_name)

    if np.abs(p[' center_ori'] - p[' surr_ori'])==0:
	block = 'para'
    elif np.abs(p[' center_ori'] - p[' surr_ori'])>0:
	block = 'ortho'
    if p[' surr_contrast'] == 0:
	block= 'none'
    
    base_conds = []
    for x in p['center_contrast'].split(' '):
	    # This is probably not the safest way to do this:
	    try:
		    base_conds.append(float(x))
	    except:
		    pass

    # Organize the contrasts according to their conditions:
    base_idx = (data_rec['surround'] == 'd').astype(int)
    comp_idx = (data_rec['surround'] == 'u').astype(int)
    base_contrasts = []
    comp_contrasts = []
    for i, x in enumerate(np.vstack([data_rec['contrast1'],
				     data_rec['contrast2']]).T):
	base_contrasts.append(x[base_idx[i]])
	comp_contrasts.append(x[comp_idx[i]])

    base_contrasts = np.array(base_contrasts)
    comp_contrasts = np.array(comp_contrasts)	

    base_conds = np.unique(base_conds)

    if fig_name is not None: 
	fig, ax = plt.subplots(1)
	colors = ['b', 'g', 'r']

    for base_idx, base_contrast in enumerate(base_conds):    
	data_idx = np.where(base_contrasts==base_contrast)
	this_comp = comp_contrasts[data_idx]
	this_ans = data_rec['answer'][data_idx] - comp_idx[data_idx]
	x = np.unique(this_comp)
	y = []
	n = []
	for c in x: 
	    idx = np.where(this_comp == c)
	    n.append(float(len(idx[0])))
	    y.append(len(np.where(this_ans[idx] == 1)[0])/n[-1])
	initial = 0,0.5
	params, _ = opt.leastsq(err_func, initial, args=(x, y, cumgauss))
	params_out.append([base_contrast, params])

        boot_th = []
        boot_sl = []
	
        # Bootstrap estimate the parameters
        for b in range(boot):
            # Choose this boot sample
	    boot_idx = np.random.randint(0, len(this_comp), len(this_comp))
	    boot_comp = this_comp[boot_idx]
	    boot_ans = this_ans[boot_idx]
	    x = np.unique(boot_comp)
	    y = []
	    n = []
	    for c in x: 
		idx = np.where(boot_comp == c)
		n.append(float(len(idx[0])))
		y.append(len(np.where(boot_ans[idx] == 1)[0])/n[-1])
	    initial = 0,0.5
	    params, _ = opt.leastsq(err_func, initial, args=(x, y, cumgauss))
	    
            boot_th.append(params[0])
            boot_sl.append(params[1])
            
        sort_th = np.sort(boot_th)
        sort_sl = np.sort(boot_sl)

        boot_th_ub = sort_th[0.84*boot]
        boot_th_lb = sort_th[0.16*boot]
        boot_sl_ub = sort_sl[0.84*boot]
        boot_sl_lb = sort_sl[0.16*boot]

	if fig_name is not None:
	    x_fine = np.arange(0,1,0.01)
	    ax.plot(x_fine, cumgauss(x_fine, params[0], params[1]))
	    ax.plot(x,y, 'o', color=colors[base_idx])
	    ax.set_xlim([0,1])
	    ax.plot([base_contrast, base_contrast],
		    [0,1], '--', color=colors[base_idx])
	    ax.text(0.7, 0.1 + 0.05 * base_idx,
		    'PSE: %.2f+/-%.2f, JND: %.2f+/-%.2f'%(params_out[-1][1][0],
							  boot_th_ub-boot_th_lb,
							  params_out[-1][1][1],
							  boot_sl_ub-boot_sl_lb))
    ax.set_title(block)	    
    fig.savefig(fig_name)
	    
    return block, params_out


## def analyze(file_name):
##     """
##     Analysis of data from hemi-field experiments
##     """
##     # Get the data from file:
##     p, l, data_rec = tools.get_data(file_name)

##     # In each trial, mark by 0/1 which (contrast1 or contrast2) is the base
##     # contrast (the surrounded stimulus) and which is the comparison contrast
##     # (the unsurrounded stimulus):
##     base_idx = (data_rec['surround'] == 'd').astype(int)
##     comp_idx = (data_rec['surround'] == 'u').astype(int)

##     # Make arrays holding these values by trial: 
##     base_contrasts = []
##     comp_contrasts = []
##     for i, x in enumerate(np.vstack([data_rec['contrast1'],
##                                      data_rec['contrast2']]).T):
        
##         base_contrasts.append(x[base_idx[i]])
##         comp_contrasts.append(x[comp_idx[i]])

##     base_contrasts = np.array(base_contrasts)
##     comp_contrasts = np.array(comp_contrasts)

##     # What are the different base conditions for which we generate separate
##     # analyses? 
##     base_conds = np.unique(base_contrasts)

##     fig, ax = plt.subplots(1)
##     colors = ['b', 'g', 'r']
##     for base_idx, base_contrast in enumerate(base_conds):    
##         data_idx = np.where(base_contrasts==base_contrast)
##         this_comp = comp_contrasts[data_idx]
##         this_ans = data_rec['answer'][data_idx] - comp_idx[data_idx]
##         x = np.unique(this_comp)
##         y = []
##         n = []
##         for c in x: 
##             idx = np.where(this_comp == c)
##             n.append(float(len(idx[0])))
##             y.append(len(np.where(this_ans[idx] == 1)[0])/n[-1])
##         initial = 0,0.5
##         params, _ = opt.leastsq(err_func, initial, args=(x, y, cumgauss))
##         print params
##         x_fine = np.arange(0,1,0.01)
##         ax.plot(x_fine, cumgauss(x_fine, params[0], params[1]))
##         ax.plot(x,y, 'o', color=colors[base_idx])
##         ax.set_xlim([0,1])
##         ax.plot([base_contrast, base_contrast],[0,1], '--',
##                 color=colors[base_idx])