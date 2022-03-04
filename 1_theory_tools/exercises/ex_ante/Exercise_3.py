# import packages used
import numpy as np
import scipy.optimize as optimize

def solve_consumption_grid_search(par):
     # initialize solution class
    class sol: pass
    sol.C = np.zeros(par.num_W)
    sol.V = np.zeros(par.num_W)
    
    # consumption grid as a share of available resources
    grid_C = np.linspace(0.0,1.0,par.num_C) 
    
    # Resource grid
    grid_W = par.grid_W

    # Init for VFI
    delta = 1000 #difference between V_next and V_now
    it = 0  #iteration counter 
    
    while (par.max_iter>= it and par.tol<delta):
        it = it+1
        V_next = sol.V.copy() #creates a copy of sol.V
        for iw,w in enumerate(grid_W):  # enumerate automaticcaly unpack w
            #Fill in start  
            c = grid_C*w # For each possible w, look at each possible c
            c_next = w - c
            
            # np.interp(x_interp,x_known,f_known)
            V_guess = np.sqrt(c)+par.beta*np.interp(c_next,grid_W,V_next) # In order to interpolate use:  np.interp.
            index = np.argmax(V_guess)
            sol.C[iw] = c[index]
            sol.V[iw] = np.amax(V_guess)
            #Fill in end
            
        delta = np.amax(np.abs(sol.V - V_next))
    
    return sol