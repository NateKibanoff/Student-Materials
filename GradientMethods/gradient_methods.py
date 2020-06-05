# solutions.py
"""Volume 2: Gradient Descent Methods.
Nathan Kibanoff
BUDS Training Program
11 November 2019
"""
import numpy as np
from scipy import linalg as la, optimize as opt

# Problem 1
def steepest_descent(f, Df, x0, tol=1e-5, maxiter=100):
    """Compute the minimizer of f using the exact method of steepest descent.

    Parameters:
        f (function): The objective function. Accepts a NumPy array of shape
            (n,) and returns a float.
        Df (function): The first derivative of f. Accepts and returns a NumPy
            array of shape (n,).
        x0 ((n,) ndarray): The initial guess.
        tol (float): The stopping tolerance.
        maxiter (int): The maximum number of iterations to compute.

    Returns:
        ((n,) ndarray): The approximate minimum of f.
        (bool): Whether or not the algorithm converged.
        (int): The number of iterations computed.
    """
    x0=np.array(x0,dtype=np.float64)
    converged=False
    k=0
    d=Df(x0)
    f1=lambda a:f(x0-a*d.T)
    while la.norm(d,np.inf)>=tol and k<=maxiter:
        a=opt.minimize_scalar(f1).x
        x0-=a*d.T
        k+=1
        d=Df(x0)
        if la.norm(d,np.inf)<tol:
            converged=True
    if not converged:
        k-=1
    return x0,converged,k

# Problem 2
def conjugate_gradient(Q, b, x0, tol=1e-4):
    """Solve the linear system Qx = b with the conjugate gradient algorithm.

    Parameters:
        Q ((n,n) ndarray): A positive-definite square matrix.
        b ((n, ) ndarray): The right-hand side of the linear system.
        x0 ((n,) ndarray): An initial guess for the solution to Qx = b.
        tol (float): The convergence tolerance.

    Returns:
        ((n,) ndarray): The solution to the linear system Qx = b.
        (bool): Whether or not the algorithm converged.
        (int): The number of iterations computed.
    """
    Q=np.array(Q,dtype=np.float64)
    b=np.array(b,dtype=np.float64)
    x0=np.array(x0,dtype=np.float64)
    converged=False
    r0=Q@x0-b
    d=-r0
    k=0
    while la.norm(r0)>=tol and k<=len(b):
        a=(r0.T@r0)/(d.T@Q@d)
        x0+=a*d
        r1=r0+a*Q@d
        beta=(r1.T@r1)/(r0.T@r0)
        d=-r1+beta*d
        k+=1
        r0=r1
        if la.norm(r0)<tol:
            converged=True
    if not converged:
        k-=1
    return x0,converged,k

'''Q=np.array([[2,0],[0,4]])
b=np.array([1,8])
x0=np.random.random(2)
print(conjugate_gradient(Q,b,x0))

f=lambda x:x[0]**2+2*x[1]**2-x[0]-8*x[1]
Df=lambda x:np.array([2*x[0]-1,4*x[1]-8])
print(steepest_descent(f,Df,x0))'''

# Problem 3
def nonlinear_conjugate_gradient(f, df, x0, tol=1e-5, maxiter=100):
    """Compute the minimizer of f using the nonlinear conjugate gradient
    algorithm.

    Parameters:
        f (function): The objective function. Accepts a NumPy array of shape
            (n,) and returns a float.
        Df (function): The first derivative of f. Accepts and returns a NumPy
            array of shape (n,).
        x0 ((n,) ndarray): The initial guess.
        tol (float): The stopping tolerance.
        maxiter (int): The maximum number of iterations to compute.

    Returns:
        ((n,) ndarray): The approximate minimum of f.
        (bool): Whether or not the algorithm converged.
        (int): The number of iterations computed.
    """
    x0=np.array(x0,dtype=np.float64)
    r=-df(x0).T
    d=r
    f1=lambda a:f(x0+a*d)
    a=opt.minimize_scalar(f1).x
    x0+=a*d
    k=1
    converged=False
    while la.norm(r)>=tol and k<maxiter:
        #print("a =",a)
        r1=-df(x0).T
        beta=(r1.T@r1)/(r.T@r)
        d=r1+beta*d
        f1=lambda a:f(x0+a*d@x0)
        a=opt.minimize_scalar(f1).x
        x0+=a*d
        r=r1
        k+=1
        if la.norm(r)<tol:
            converged=True
        #print(f(x0))
    return x0,converged,k

print(opt.fmin_cg(opt.rosen,np.array([10,10]),fprime=opt.rosen_der))
print("===========================")
print(nonlinear_conjugate_gradient(opt.rosen,opt.rosen_der,np.array([10,10]),maxiter=50000))
#print(steepest_descent(opt.rosen,opt.rosen_der,np.array([10,10]),maxiter=10000))

# Problem 4
def prob4(filename="linregression.txt",
          x0=np.array([-3482258, 15, 0, -2, -1, 0, 1829],dtype=np.float64)):
    """Use conjugate_gradient() to solve the linear regression problem with
    the data from the given file, the given initial guess, and the default
    tolerance. Return the solution to the corresponding Normal Equations.
    """
    data=np.loadtxt(filename)
    y=data[:,0]
    x=np.column_stack((np.ones(len(data)),data[:,1:]))
    print(x.T.shape)
    print(x.shape)
    return conjugate_gradient(x.T@x,x.T@y,x0)[0]
#print(prob4())

# Problem 5
class LogisticRegression1D:
    """Binary logistic regression classifier for one-dimensional data."""

    def fit(self, x, y, guess):
        """Choose the optimal beta values by minimizing the negative log
        likelihood function, given data and outcome labels.

        Parameters:
            x ((n,) ndarray): An array of n predictor variables.
            y ((n,) ndarray): An array of n outcome variables.
            guess (array): Initial guess for beta.
        """
        raise NotImplementedError("Problem 5 Incomplete")

    def predict(self, x):
        """Calculate the probability of an unlabeled predictor variable
        having an outcome of 1.

        Parameters:
            x (float): a predictor variable with an unknown label.
        """
        raise NotImplementedError("Problem 5 Incomplete")


# Problem 6
def prob6(filename="challenger.npy", guess=np.array([20., -1.])):
    """Return the probability of O-ring damage at 31 degrees Farenheit.
    Additionally, plot the logistic curve through the challenger data
    on the interval [30, 100].

    Parameters:
        filename (str): The file to perform logistic regression on.
                        Defaults to "challenger.npy"
        guess (array): The initial guess for beta.
                        Defaults to [20., -1.]
    """
    raise NotImplementedError("Problem 6 Incomplete")
