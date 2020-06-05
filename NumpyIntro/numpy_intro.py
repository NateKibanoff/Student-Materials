# numpy_intro.py
"""Python Essentials: Intro to NumPy.
Nathan Kibanoff
BUDS Training Program
29 July 2019
"""
import numpy as np

def prob1():
    """Define the matrices A and B as arrays. Return the matrix product AB."""
    A=np.array([[3,-1,4],[1,5,-9]])
    B=np.array([[2,6,-5,3],[5,-8,9,7],[9,-3,-2,-3]])
    return A@B
    raise NotImplementedError("Problem 1 Incomplete")

def prob2():
    """Define the matrix A as an array. Return the matrix -A^3 + 9A^2 - 15A."""
    A=np.array([[3,1,4],[1,5,9],[-5,3,1]])
    return -(A@A@A)+9*(A@A)-15*A
    raise NotImplementedError("Problem 2 Incomplete")

def prob3():
    """Define the matrices A and B as arrays. Calculate the matrix product ABA,
    change its data type to np.int64, and return it.
    """
    all_ones=np.ones((7,7))
    diag_ones=np.diag(np.ones(7))
    A=np.triu(all_ones)
    B=5*np.triu(all_ones)-np.tril(all_ones)-5*diag_ones
    return np.int64(A@B@A)
    raise NotImplementedError("Problem 3 Incomplete")

def prob4(A):
    """Make a copy of 'A' and set all negative entries of the copy to 0.
    Return the copy.
    Example:
        >>> A = np.array([-3,-1,3])
        >>> prob4(A)
        array([0, 0, 3])
    """
    B=A.copy()
    B[B<0]=0
    return B
    raise NotImplementedError("Problem 4 Incomplete")

def prob5():
    """Define the matrices A, B, and C as arrays. Return the block matrix
                                | 0 A^T I |
                                | A  0  0 |,
                                | B  0  C |
    where I is the 3x3 identity matrix and each 0 is a matrix of all zeros
    of the appropriate size.
    """
    A=np.arange(0,6).reshape((3,2)).T
    B=3*np.tril(np.ones((3,3),dtype=np.int64))
    I=np.diag(np.ones(3,dtype=np.int64))
    C=-2*I
    zero33=np.zeros((3,3),dtype=np.int64)
    zero22=np.zeros((2,2),dtype=np.int64)
    zero23=np.zeros((2,3),dtype=np.int64)
    return np.vstack((np.hstack((zero33,A.T,I)),np.hstack((A,zero22,zero23)),np.hstack((B,zero23.T,C))))
    raise NotImplementedError("Problem 5 Incomplete")

def prob6(A):
    """Divide each row of 'A' by the row sum and return the resulting array.
    Example:
        >>> A = np.array([[1,1,0],[0,1,0],[1,1,1]])
        >>> prob6(A)
        array([[ 0.5       ,  0.5       ,  0.        ],
               [ 0.        ,  1.        ,  0.        ],
               [ 0.33333333,  0.33333333,  0.33333333]])
    """
    divisors=A.sum(axis=1).reshape((-1,1))
    return A/divisors
    raise NotImplementedError("Problem 6 Incomplete")

def prob7():
    """Given the array stored in grid.npy, return the greatest product of four
    adjacent numbers in the same direction (up, down, left, right, or
    diagonally) in the grid.
    """
    grid=np.load("grid.npy")
    horizontal=np.max(grid[:,:-3]*grid[:,1:-2]*grid[:,2:-1]*grid[:,3:])
    vertical=np.max(grid[:-3,:]*grid[1:-2,:]*grid[2:-1,:]*grid[3:,:])
    left_diagonal=np.max(grid[:-3,:-3]*grid[1:-2,1:-2]*grid[2:-1,2:-1]*grid[3:,3:])
    right_diagonal=np.max(grid[:-3,3:]*grid[1:-2,2:-1]*grid[2:-1,1:-2]*grid[3:,:-3])
    return max(horizontal,vertical,left_diagonal,right_diagonal)
    raise NotImplementedError("Problem 7 Incomplete")
