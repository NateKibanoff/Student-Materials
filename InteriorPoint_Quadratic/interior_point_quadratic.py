# interior_point_quadratic.py
"""Volume 2: Interior Point for Quadratic Programs.
Nathan Kibanoff
BUDS Training Program
11 November 2019
"""

import numpy as np
from scipy import linalg as la
from scipy.sparse import spdiags

def startingPoint(G, c, A, b, guess):
    """
    Obtain an appropriate initial point for solving the QP
    .5 x^T Gx + x^T c s.t. Ax >= b.
    Parameters:
        G -- symmetric positive semidefinite matrix shape (n,n)
        c -- array of length n
        A -- constraint matrix shape (m,n)
        b -- array of length m
        guess -- a tuple of arrays (x, y, mu) of lengths n, m, and m, resp.
    Returns:
        a tuple of arrays (x0, y0, l0) of lengths n, m, and m, resp.
    """
    m,n = A.shape
    x0, y0, l0 = guess

    # Initialize linear system
    N = np.zeros((n+m+m, n+m+m))
    N[:n,:n] = G
    N[:n, n+m:] = -A.T
    N[n:n+m, :n] = A
    N[n:n+m, n:n+m] = -np.eye(m)
    N[n+m:, n:n+m] = np.diag(l0)
    N[n+m:, n+m:] = np.diag(y0)
    rhs = np.empty(n+m+m)
    rhs[:n] = -(G.dot(x0) - A.T.dot(l0)+c)
    rhs[n:n+m] = -(A.dot(x0) - y0 - b)
    rhs[n+m:] = -(y0*l0)

    sol = la.solve(N, rhs)
    dx = sol[:n]
    dy = sol[n:n+m]
    dl = sol[n+m:]

    y0 = np.maximum(1, np.abs(y0 + dy))
    l0 = np.maximum(1, np.abs(l0+dl))

    return x0, y0, l0


# Problems 1-2
def qInteriorPoint(Q, c, A, b, guess, niter=20, tol=1e-16, verbose=False):
    """Solve the Quadratic program min .5 x^T Q x +  c^T x, Ax >= b
    using an Interior Point method.

    Parameters:
        Q ((n,n) ndarray): Positive semidefinite objective matrix.
        c ((n, ) ndarray): linear objective vector.
        A ((m,n) ndarray): Inequality constraint matrix.
        b ((m, ) ndarray): Inequality constraint vector.
        guess (3-tuple of arrays of lengths n, m, and m): Initial guesses for
            the solution x and lagrange multipliers y and eta, respectively.
        niter (int > 0): The maximum number of iterations to execute.
        tol (float > 0): The convergence tolerance.

    Returns:
        x ((n, ) ndarray): The optimal point.
        val (float): The minimum value of the objective function.
    """
    m,n = A.shape
    def F(x_, l_, m_):
        """The almost-linear function that accounts for the KKT conditions."""
        return np.hstack(((A.T @ l_)+m_-c, (A @ x_)-b, m_*x_))

    DF = np.zeros((2*n+m, 2*n+m))
    DF[:n,n:-n] = A.T
    DF[:n,-n:] = np.eye(n)
    DF[n:-n,:n] = A

    # Get the initial point and verify the dimensions.
    x, lam, mu = startingPoint(A, b, c)
    assert len(x) == len(mu) == len(c) == n
    assert len(lam) == len(b) == m

    e = np.ones_like(mu)
    sigma = .1

    i = 0
    nu = 1 + tol
    while i < niter and nu >= tol:
        i += 1

        # Problem 3: Search Direction
        DF[-n:,:n] = np.diag(mu)
        DF[-n:,-n:] = np.diag(x)

        nu = (x @ mu) / n
        nu_vec = np.hstack((np.zeros(n+m), e*nu*sigma))
        lu_piv = la.lu_factor(DF)
        direct = la.lu_solve(lu_piv, nu_vec - F(x,lam,mu))

        # Problem 4: Step Length
        dx, dlam, dmu = direct[:n], direct[n:-n], direct[-n:]

        mask = dmu < 0
        amin = np.min(-mu[mask]/dmu[mask])
        alpha = min(1, .95*min(1, amin)) if np.any(mask) else .95

        mask = dx < 0
        dmin = np.min(-x[mask]/dx[mask]).min()
        delta = min(1, .95*min(1, dmin)) if np.any(mask) else .95

        # Problem 5: Finish it up.
        x += delta*dx
        lam += alpha*dlam
        mu += alpha*dmu

        if verbose:
            print("Iteration {:0>2} nu = {}".format(i, nu))
    if i < niter and verbose:
        print("Converged in {} iterations".format(i))
    elif verbose:
        print("Maximum iterations reached")
    return x, c.dot(x)

def laplacian(n):
    """Construct the discrete Dirichlet energy matrix H for an n x n grid."""
    data = -1*np.ones((5, n**2))
    data[2,:] = 4
    data[1, n-1::n] = 0
    data[3, ::n] = 0
    diags = np.array([-n, -1, 0, 1, n])
    return spdiags(data, diags, n**2, n**2).toarray()


# Problem 3
def circus(n=15):
    """Solve the circus tent problem for grid size length 'n'.
    Display the resulting figure.
    """
    raise NotImplementedError("Problem 3 Incomplete")


# Problem 4
def portfolio(filename="portfolio.txt"):
    """Markowitz Portfolio Optimization

    Parameters:
        filename (str): The name of the portfolio data file.

    Returns:
        (ndarray) The optimal portfolio with short selling.
        (ndarray) The optimal portfolio without short selling.
    """
    raise NotImplementedError("Problem 4 Incomplete")
