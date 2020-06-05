# newtons_method.py
"""Volume 1: Newton's Method.
Nathan Kibanoff
BUDS Training Program
28 August 2019
"""
import numpy as np
from scipy import optimize as op
from matplotlib import pyplot as plt
from scipy import linalg as la

# Problems 1, 3, and 5
def newton(f, x0, Df, tol=1e-5, maxiter=15, alpha=1.):
    """Use Newton's method to approximate a zero of the function f.

    Parameters:
        f (function): a function from R^n to R^n (assume n=1 until Problem 5).
        x0 (float or ndarray): The initial guess for the zero of f.
        Df (function): The derivative of f, a function from R^n to R^(nxn).
        tol (float): Convergence tolerance. The function should return when
            the difference between successive approximations is less than tol.
        maxiter (int): The maximum number of iterations to compute.
        alpha (float): Backtracking scalar (Problem 3).

    Returns:
        (float or ndarray): The approximation for a zero of f.
        (bool): Whether or not Newton's method converged.
        (int): The number of iterations computed.
    """
    i=0
    converged=False
    #print(x0.shape)
    if np.isscalar(x0):
        while i<maxiter:
            xk=x0-alpha*f(x0)/Df(x0)
            i+=1
            x0=xk
            if abs(xk-x0)<tol:
                converged=True
                break
    else:
        while i<maxiter:
            if np.allclose(la.det(Df(x0)),0):
                return x0,converged,i
            yk=la.solve(Df(x0),f(x0))
            #print(yk.shape)
            xk=x0-alpha*yk.T
            #print(xk.shape)
            #print()
            i+=1
            x0=xk
            if la.norm(xk-x0)<tol:
                converged=True
                break
    return x0,converged,i

# Problem 2
def prob2(N1, N2, P1, P2):
    """Use Newton's method to solve for the constant r that satisfies

                P1[(1+r)**N1 - 1] = P2[1 - (1+r)**(-N2)].

    Use r_0 = 0.1 for the initial guess.

    Parameters:
        N1 (int): Number of years money is deposited.
        N2 (int): Number of years money is withdrawn.
        P1 (float): Amount of money deposited into account at the beginning of
            years 1, 2, ..., N1.
        P2 (float): Amount of money withdrawn at the beginning of years N1+1,
            N1+2, ..., N1+N2.

    Returns:
        (float): the value of r that satisfies the equation.
    """
    f=lambda r:P2-P2*(1+r)**(-N2)-P1*(1+r)**N1+P1
    Df=lambda r:N2*P2*(1+r)**(-N2-1)-N1*P1*(1+r)**(N1-1)
    return newton(f,0.1,Df)[0]

# Problem 4
def optimal_alpha(f, x0, Df, tol=1e-5, maxiter=15):
    """Run Newton's method for various values of alpha in (0,1].
    Plot the alpha value against the number of iterations until convergence.

    Parameters:
        f (function): a function from R^n to R^n (assume n=1 until Problem 5).
        x0 (float or ndarray): The initial guess for the zero of f.
        Df (function): The derivative of f, a function from R^n to R^(nxn).
        tol (float): Convergence tolerance. The function should returns when
            the difference between successive approximations is less than tol.
        maxiter (int): The maximum number of iterations to compute.

    Returns:
        (float): a value for alpha that results in the lowest number of
            iterations.
    """
    alpha=np.linspace(0,1)
    iters=[]
    min_iter=maxiter+1
    min_alpha=0
    for i in range(1,len(alpha)):
        iters.append(newton(f,x0,Df,tol,maxiter,alpha[i])[2])
        if iters[i-1]<min_iter:
            min_iter=iters[i-1]
            min_alpha=alpha[i-1]
    plt.plot(alpha,iters)
    plt.show()
    return min_alpha

# Problem 6
def prob6():
    """Consider the following Bioremediation system.

                              5xy − x(1 + y) = 0
                        −xy + (1 − y)(1 + y) = 0

    Find an initial point such that Newton’s method converges to either
    (0,1) or (0,−1) with alpha = 1, and to (3.75, .25) with alpha = 0.55.
    Return the intial point as a 1-D NumPy array with 2 entries.
    """
    f=lambda x:np.array([[5*x[0]*x[1]-x[0]*(1+x[1])],[-x[0]*x[1]+(1-x[1]**2)]])
    Df=lambda x:np.array([[4*x[1]-1,4*x[0]],[-x[1],-2*x[1]-x[0]]])
    x=np.linspace(-0.25,0)
    y=np.linspace(0,0.25)
    sol1=np.array([[0,1]])
    sol2=np.array([[0,-1]])
    sol3=np.array([[3.75,0.25]])
    for i in range(len(x)):
        for j in range(len(y)):
            x0=np.array([x[i],y[j]])
            a1=newton(f,x0,Df)[0]
            a2=newton(f,x0,Df,alpha=0.55)[0]
            #print(a1,a2)
            if (np.allclose(a1,sol1) or np.allclose(a1,sol2)) and np.allclose(a2,sol3):
                return x0

# Problem 7
def plot_basins(f, Df, zeros, domain, res=1000, iters=15):
    """Plot the basins of attraction of f on the complex plane.

    Parameters:
        f (function): A function from C to C.
        Df (function): The derivative of f, a function from C to C.
        zeros (ndarray): A 1-D array of the zeros of f.
        domain ([r_min, r_max, i_min, i_max]): A list of scalars that define
            the window limits and grid domain for the plot.
        res (int): A scalar that determines the resolution of the plot.
            The visualized grid has shape (res, res).
        iters (int): The exact number of times to iterate Newton's method.
    """
    real=np.linspace(domain[0],domain[1],res)
    imag=np.linspace(domain[2],domain[3],res)
    rmesh,imesh=np.meshgrid(real,imag)
    x0=rmesh+1j*imesh
    for i in range(iters):
        x0=x0-f(x0)/Df(x0)
    Y=[]
    for i in range(res):
        Y.append([])
        for j in range(res):
            closest=np.abs(x0[i][j]-zeros)
            Y[i].append(np.argmin(closest))
    plt.pcolormesh(rmesh,imesh,Y,cmap="brg")
    plt.show()
