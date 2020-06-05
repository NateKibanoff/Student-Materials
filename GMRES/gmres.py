# gmres.py
"""Volume 1: GMRES.
Nathan Kibanoff
BUDS Training Program
4 November 2019
"""
import numpy as np
from scipy import linalg as la
from matplotlib import pyplot as plt
from scipy.sparse import linalg as spla
import time

# Problems 1 and 2.
def gmres(A, b, x0, k=100, tol=1e-8, plot=False):
    """Calculate approximate solution of Ax=b using the GMRES algorithm.

    Parameters:
        A ((m,m) ndarray): A square matrix.
        b ((m,) ndarray): A 1-D array of length m.
        x0 ((m,) ndarray): The initial guess for the solution to Ax=b.
        k (int): Maximum number of iterations of the GMRES algorithm.
        tol (float): Stopping criterion for size of residual.
        plot (bool): Whether or not to plot convergence (Problem 2).

    Returns:
        ((m,) ndarray): Approximate solution to Ax=b.
        res (float): Residual of the solution.
    """
    iters=[]
    real=0
    imag=0
    if plot:
        eigs=la.eig(A)[0]
        real=eigs.real
        imag=eigs.imag
    Q=np.empty((b.size,k+1))
    H=np.zeros((k+1,k))
    r0=b-A@x0
    Q[:,0]=r0/la.norm(r0)
    res=[]
    beta=la.norm(b-A@x0)
    e=np.zeros(k+1)
    e[0]=1
    for j in range(k):
        iters.append(j+1)
        Q[:,j+1]=A@Q[:,j]
        for i in range(j+1):
            H[i,j]=Q[:,i].T@Q[:,j+1]
            Q[:,j+1]-=H[i,j]*Q[:,i]
        H[j+1,j]=la.norm(Q[:,j+1])
        if abs(H[j+1,j])>tol:
            Q[:,j+1]/=H[j+1,j]
        y=la.lstsq(H[:j+2,:j+1],beta*e[:j+2])[0]
        res.append(la.norm(H[:j+2,:j+1]@y-beta*e[:j+2]))
        if res[j]<tol:
            if plot:
                p1=plt.subplot(121)
                p1.scatter(real,imag)
                p1.set_title("Eigenvalues of A on the complex plane")
                p1.set_xlabel("Real components")
                p1.set_ylabel("Imaginary components")
                p2=plt.subplot(122)
                p2.semilogy(iters,res)
                p2.set_title("Computed residuals per iteration")
                p2.set_xlabel("Number of iterations")
                p2.set_ylabel("log(Residuals)")
                plt.show()
            return Q[:,:j+1]@y+x0,res[j]
    if plot:
        p1=plt.subplot(121)
        p1.scatter(real,imag)
        p1.set_title("Eigenvalues of A on the complex plane")
        p1.set_xlabel("Real components")
        p1.set_ylabel("Imaginary components")
        p2=plt.subplot(122)
        p2.semilogy(iters,res)
        p2.set_title("Computed residuals per iteration")
        p2.set_xlabel("Number of iterations")
        p2.set_ylabel("log(Residuals)")
        plt.show()
    return Q[:,:j+1]@y+x0,res[k-1]

# Problem 3
def prob3(m=200):
    """For n=-4,-2,0,2,4 create a matrix A= n*I + P where I is the mxm
    identity, and P is an mxm matrix with entries drawn from a normal
    distribution with mean 0 and standard deviation 1/(2*sqrt(m)).
    For each of the given values of n call gmres() with A, a vector of ones called b, an initial guess x0=0, and plot=True

    Parameters:
        m (int): Size of the matrix A.
    """
    for n in range(-4,5,2):
        A=n*np.identity(m)+np.random.normal(0,1/(2*np.sqrt(m)),(m,m))
        gmres(A,np.ones(m),np.zeros(m),plot=True)

# Problem 4
def gmres_k(A, b, x0, k=5, tol=1E-8, restarts=50):
    """Implement the GMRES algorithm with restarts. Terminate the algorithm
    when the size of the residual is less than tol or when the maximum number
    of restarts has been reached.

    Parameters:
        A ((m,m) ndarray): A square matrix.
        b ((m,) ndarray): A 1-D array of length m.
        x0 ((m,) ndarray): The initial guess for the solution to Ax=b.
        k (int): Maximum number of iterations of the GMRES algorithm.
        tol (float): Stopping criterion for size of residual.
        restarts (int): Maximum number of restarts. Defaults to 50.

    Returns:
        ((m,) ndarray): Approximate solution to Ax=b.
        res (float): Residual of the solution.
    """
    res=0
    while restarts>0:
        x0,res=gmres(A,b,x0,k,tol)
        if res<tol:
            return x0,res
        restarts-=1
    return x0,res

# Problem 5
def time_gmres(m=200):
    """Using the same matrices as in problem 2, plot the time required to
    complete gmres(), gmres_k(), and scipy.sparse.linalg.gmres() with
    restarts. Plot the values of n against the times.

    Parameters:
        m (int): Size of matrix A.
    """
    n=[]
    t1=[]
    t2=[]
    t3=[]
    for i in range(25,m+1,25):
        n.append(i)
        A=np.random.normal(0,1/(2*np.sqrt(i)),(i,i))
        b=np.ones(i)
        x0=np.zeros(i)

        t1.append(time.time())
        gmres(A,b,x0)
        t1[i//25-1]=time.time()-t1[i//25-1]

        t2.append(time.time())
        gmres_k(A,b,x0)
        t2[i//25-1]=time.time()-t2[i//25-1]

        t3.append(time.time())
        spla.gmres(A,b,restart=1000)
        t3[i//25-1]=time.time()-t3[i//25-1]

    plt.plot(n,t1,label="gmres")
    plt.plot(n,t2,label="gmres_k")
    plt.plot(n,t3,label="scipy.sparse.linalg.gmres")
    plt.title("Runtime of different versions of the GMRES algorithm")
    plt.xlabel("Size of matrix")
    plt.ylabel("Runtime (seconds)")
    plt.legend()
    plt.show()
