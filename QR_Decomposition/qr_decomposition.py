# qr_decomposition.py
"""Volume 1: The QR Decomposition.
Nathan Kibanoff
BUDS Training Program
1 September 2019
"""
import numpy as np
from scipy import linalg as la

# Problem 1
def qr_gram_schmidt(A):
    """Compute the reduced QR decomposition of A via Modified Gram-Schmidt.

    Parameters:
        A ((m,n) ndarray): A matrix of rank n.

    Returns:
        Q ((m,n) ndarray): An orthonormal matrix.
        R ((n,n) ndarray): An upper triangular matrix.
    """
    m,n=A.shape
    Q=np.copy(A)
    R=np.zeros((n,n))
    for i in range(n):
        R[i,i]=la.norm(Q[:,i])
        Q[:,i]/=R[i,i]
        for j in range(i+1,n):
            R[i,j]=Q[:,j].T@Q[:,i]
            Q[:,j]-=R[i,j]*Q[:,i]
    return Q,R

# Problem 2
def abs_det(A):
    """Use the QR decomposition to efficiently compute the absolute value of
    the determinant of A.

    Parameters:
        A ((n,n) ndarray): A square matrix.

    Returns:
        (float) the absolute value of the determinant of A.
    """
    return abs(np.prod(np.diag(qr_gram_schmidt(A)[1])))

# Problem 3
def solve(A, b):
    """Use the QR decomposition to efficiently solve the system Ax = b.

    Parameters:
        A ((n,n) ndarray): An invertible matrix.
        b ((n, ) ndarray): A vector of length n.

    Returns:
        x ((n, ) ndarray): The solution to the system Ax = b.
    """
    n=A.shape[0]
    Q,R=qr_gram_schmidt(A)
    y=Q.T@b
    x=np.random.random((n,1))
    for i in range(n-1,-1,-1):
        x_n=y[i,0]
        for j in range(i+1,n):
            x_n-=R[i,j]*x[j,0]
        x[i,0]=x_n/R[i,i]
    return x

# Problem 4
def qr_householder(A):
    """Compute the full QR decomposition of A via Householder reflections.

    Parameters:
        A ((m,n) ndarray): A matrix of rank n.

    Returns:
        Q ((m,m) ndarray): An orthonormal matrix.
        R ((m,n) ndarray): An upper triangular matrix.
    """
    sign=lambda x:1 if x>=0 else -1
    m,n=A.shape
    R=np.copy(A)
    Q=np.identity(m)
    for k in range(n):
        u=np.copy(R[k:,k]) # m-k x 1
        u[0]+=sign(u[0])*la.norm(u)
        u/=la.norm(u)
        R[k:,k:]-=np.outer(2*u,u.T@R[k:,k:])
        Q[k:,:]-=np.outer(2*u,u.T@Q[k:,:])
    return Q.T,R

# Problem 5
def hessenberg(A):
    """Compute the Hessenberg form H of A, along with the orthonormal matrix Q
    such that A = QHQ^T.

    Parameters:
        A ((n,n) ndarray): An invertible matrix.

    Returns:
        H ((n,n) ndarray): The upper Hessenberg form of A.
        Q ((n,n) ndarray): An orthonormal matrix.
    """
    sign=lambda x:1 if x>=0 else -1
    m,n=A.shape
    H=np.copy(A)
    Q=np.identity(m)
    for k in range(n-2):
        u=np.copy(H[k+1:,k])
        u[0]+=sign(u[0])*la.norm(u)
        u/=la.norm(u)
        H[k+1:,k:]-=2*np.outer(u,u.T@H[k+1:,k:])
        H[:,k+1:]-=2*np.outer(H[:,k+1:]@u,u.T)
        Q[k+1:,:]-=2*np.outer(u,u.T@Q[k+1:,:])
    return H,Q.T
