# lstsq_eigs.py
"""Volume 1: Least Squares and Computing Eigenvalues.
Nathan Kibanoff
BUDS Training Program
2 September 2019
"""
# (Optional) Import functions from your QR Decomposition lab.
#import sys
#sys.path.insert(1, "../QR_Decomposition")
#from qr_decomposition import qr_gram_schmidt, qr_householder, hessenberg

import numpy as np
from matplotlib import pyplot as plt
from scipy import linalg as la
import cmath

# Problem 1
def least_squares(A, b):
    """Calculate the least squares solutions to Ax = b by using the QR
    decomposition.

    Parameters:
        A ((m,n) ndarray): A matrix of rank n <= m.
        b ((m, ) ndarray): A vector of length m.

    Returns:
        x ((n, ) ndarray): The solution to the normal equations.
    """
    #Q,R=qr_gram_schmidt(A)
    Q,R=la.qr(A,mode="economic")
    return la.solve_triangular(R,Q.T@b)

# Problem 2
def line_fit():
    """Find the least squares line that relates the year to the housing price
    index for the data in housing.npy. Plot both the data points and the least
    squares line.
    """
    housing=np.load("housing.npy")
    years=housing.T[0]
    index=housing.T[1]
    A=np.column_stack((years,np.ones(len(years))))
    x=least_squares(A,index.T)
    y=x[0]*years+x[1]
    plt.scatter(years,index, label="Actual datapoints")
    plt.plot(years,y, label="Least squares line")
    plt.xlabel("Year")
    plt.ylabel("Housing price index")
    plt.title("Least squares line for year and housing price index")
    plt.show()

# Problem 3
def polynomial_fit():
    """Find the least squares polynomials of degree 3, 6, 9, and 12 that relate
    the year to the housing price index for the data in housing.npy. Plot both
    the data points and the least squares polynomials in individual subplots.
    """
    housing=np.load("housing.npy")
    years=housing.T[0]
    index=housing.T[1]

    A3=np.vander(years,4)
    c3=least_squares(A3,index.T)
    y3=np.poly1d(c3)

    A6=np.vander(years,7)
    c6=least_squares(A6,index.T)
    y6=np.poly1d(c6)

    A9=np.vander(years,10)
    c9=least_squares(A9,index.T)
    y9=np.poly1d(c9)

    A12=np.vander(years,13)
    c12=least_squares(A12,index.T)
    y12=np.poly1d(c12)

    plt.scatter(years,index, label="Actual datapoints")
    plt.plot(years,y3(years), label="Degree = 3")
    plt.plot(years,y6(years), label="Degree = 6")
    plt.plot(years,y9(years), label="Degree = 9")
    plt.plot(years,y12(years), label="Degree = 12")
    plt.legend()
    plt.xlabel("Year")
    plt.ylabel("Housing price index")
    plt.title("Least squares polynomials for year and housing price index")
    plt.show()

def plot_ellipse(a, b, c, d, e):
    """Plot an ellipse of the form ax^2 + bx + cxy + dy + ey^2 = 1."""
    theta = np.linspace(0, 2*np.pi, 200)
    cos_t, sin_t = np.cos(theta), np.sin(theta)
    A = a*(cos_t**2) + c*cos_t*sin_t + e*(sin_t**2)
    B = b*cos_t + d*sin_t
    r = (-B + np.sqrt(B**2 + 4*A)) / (2*A)

    plt.plot(r*cos_t, r*sin_t)
    plt.gca().set_aspect("equal", "datalim")
    plt.show()

# Problem 4
def ellipse_fit():
    """Calculate the parameters for the ellipse that best fits the data in
    ellipse.npy. Plot the original data points and the ellipse together, using
    plot_ellipse() to plot the ellipse.
    """
    ellipse=np.load("ellipse.npy")
    x=ellipse.T[0]
    y=ellipse.T[1]
    A=np.column_stack((x**2,x,x*y,y,y**2))
    params=least_squares(A,np.ones(len(x)))
    plt.scatter(x,y)
    plot_ellipse(params[0],params[1],params[2],params[3],params[4])

# Problem 5
def power_method(A, N=20, tol=1e-12):
    """Compute the dominant eigenvalue of A and a corresponding eigenvector
    via the power method.

    Parameters:
        A ((n,n) ndarray): A square matrix.
        N (int): The maximum number of iterations.
        tol (float): The stopping tolerance.

    Returns:
        (float): The dominant eigenvalue of A.
        ((n,) ndarray): An eigenvector corresponding to the dominant
            eigenvalue of A.
    """
    m,n=A.shape
    x_n=np.random.random(n)
    x_n/=la.norm(x_n)
    for k in range(N):
        x_k=A@x_n
        if la.norm(x_k-x_n)<tol:
            break
        x_n=x_k/la.norm(x_k)
    return x_n.T@A@x_n,x_n

# Problem 6
def qr_algorithm(A, N=50, tol=1e-12):
    """Compute the eigenvalues of A via the QR algorithm.

    Parameters:
        A ((n,n) ndarray): A square matrix.
        N (int): The number of iterations to run the QR algorithm.
        tol (float): The threshold value for determining if a diagonal S_i
            block is 1x1 or 2x2.

    Returns:
        ((n,) ndarray): The eigenvalues of A.
    """
    m,n=A.shape
    S=la.hessenberg(A)
    for k in range(N):
        Q,R=la.qr(S)
        S=R@Q
    eigs=[]
    i=0
    while i<n:
        if i==n-1 or abs(S[i+1][i])<tol:
            eigs.append(S[i][i])
        else:
            a=S[i][i]
            b=S[i][i+1]
            c=S[i+1][i]
            d=S[i+1][i+1]
            e1=((a+d)+cmath.sqrt((a+d)**2-4*(a*d-b*c)))/2
            e2=((a+d)-cmath.sqrt((a+d)**2-4*(a*d-b*c)))/2
            eigs.append(e1)
            eigs.append(e2)
            i+=1
        i+=1
    return eigs
