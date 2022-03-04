# import packages used
import numpy as np

def solve_consumption_uncertainty(par):
     # initialize solution class
    class sol: pass
    sol.V = np.zeros([par.num_W,par.T]) 
    sol.C = np.zeros([par.num_W,par.T])
    sol.grid_W = np.zeros([par.num_W,par.T])
    
    # consumption grid as a share of available resources
    grid_C = np.linspace(0.0,1.0,par.num_C)
    
    # Loop over periods
    for t in range(par.T-1, -1, -1):  #from period T-1, until period 0, backwards (-1)
        W_max = max(par.eps) * t + par.W # Maximum what you can get, being very very lucky. Needed to create grid_W.
        grid_W = np.linspace(0,W_max,par.num_W) # num_W is the number of grid points.
        sol.grid_W[:,t] = grid_W #See Exercise 4: Introducing unvertainty, in 001_slides_untertainty.
    
        for iw,w in enumerate(grid_W):
            c = grid_C * w
            w_c = w - c
            EV_next = 0 # For last period T. We get 0 for sure in the next period.
        
            if t<par.T-1: # excludes last period, directly stops here.
                #Fill in start
                
                for s in range(par.K): #shocks from 1 to 5

                    #weight of the shock
                    weight = par.pi[s]
                    
                    # epsilon shock
                    eps = par.eps[s]
                    
                    # expected value with this shock
                    EV_next += weight * np.interp(w_c + eps,sol.grid_W[:,t+1],sol.V[:,t+1]) #linear interpolation
                    
                    # From this loop, we get EV including all possible shocks.
                    
                  #Fill in end
            V_guess = np.sqrt(c) + par.beta * EV_next
            index = np.argmax(V_guess)
            sol.C[iw,t] = c[index]
            sol.V[iw,t] = np.amax(V_guess)
        
    return sol