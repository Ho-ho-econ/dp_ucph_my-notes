# import packages used
import numpy as np
import tools as tools
from scipy import interpolate

def setup():
    # Setup specifications in class. 
    class par: pass
    par.beta = 0.90
    par.rho = 0.5
    par.R = 1.0/par.beta
    par.sigma = 0.2
    par.mu = 0
    par.W = 10
    
    # Shocks and weights
    par.num_shocks = 5
    x,w = tools.gauss_hermite(par.num_shocks)
    par.eps = np.exp(par.sigma*np.sqrt(2)*x)
    par.eps_w = w/np.sqrt(np.pi)
    
    # Grid
    par.num_W = 200
    par.num_C = 200
    par.grid_W = np.linspace(0,par.W,par.num_W)
    
    # Parameters for VFI
    par.max_iter = 200   # maximum number of iterations
    par.tol = 10e-2 #convergence tol. level 
        
    return par


def util(c,par):
    return (c**(1.0-par.rho))/(1.0-par.rho)

def solve_deaton_infty(par):
     # initialize solution class
    class sol: pass
    sol.V = np.zeros([par.num_W]) 
    sol.C = np.zeros([par.num_W])
    
    # consumption grid as a share of available resources
    grid_C = np.linspace(0.0,1.0,par.num_C)
    
    # initialize counter
    sol.it = 0
    sol.delta = 2000

    while (par.max_iter>= sol.it and par.tol<sol.delta):
        
        V0 = sol.V.copy()
        interp = interpolate.interp1d(par.grid_W,V0, bounds_error=False, fill_value = "extrapolate") 
        #Use this instead of np.interp, because it can extrapolate outside grid
        
        for iw,w in enumerate(par.grid_W):
            #fill in start
            c = grid_C*w
            w_c = w - c

            for s in range(par.num_shocks):
                #weight of the shock
                weight = par.eps_w[s]

                # epsilon shock
                eps = par.eps[s]

                # next period assets
                w_next = par.R * w_c + eps

                V_guess = util(c,par) + par.beta * interp(w_next) # Here I get this error: "unsupported operand type(s) for *: 'float' and 'interp1d'"
                index = np.argmax(V_guess)
                sol.C[iw] = c[index]
                sol.V[iw] = np.amax(V_guess)


            # fill in end
            sol.it += 1
            sol.delta = max(abs(sol.V - V0)) 
    
    return sol