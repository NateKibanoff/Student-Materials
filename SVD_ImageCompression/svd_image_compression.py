# solutions.py
"""Volume 1: The SVD and Image Compression. Solutions File."""
import numpy as np
from scipy import linalg as la
from matplotlib import pyplot as plt
from imageio import imread

# Problem 1
def compact_svd(A, tol=1e-6):
    """Compute the truncated SVD of A.

    Parameters:
        A ((m,n) ndarray): The matrix (of rank r) to factor.
        tol (float): The tolerance for excluding singular values.

    Returns:
        ((m,r) ndarray): The orthonormal matrix U in the SVD.
        ((r,) ndarray): The singular values of A as a 1-D array.
        ((r,n) ndarray): The orthonormal matrix V^H in the SVD.
    """
    L,V=la.eig(A.conj().T@A)
    V=V.T
    s=np.sqrt(L)
    v_sort=np.argsort(-s)
    s=-np.sort(-s)
    v_copy=np.copy(V)
    for i in range(len(v_sort)):
        V[i]=v_copy[v_sort[i]]
    r=len(s)
    for i in range(len(s)-1,-1,-1):
        if s[i]>tol:
            break
        r-=1
    s=s[:r]
    V=V[:r]
    U=(A@V[0])/s[0]
    for i in range(1,r):
        U=np.column_stack((U,(A@V[i])/s[i]))
    return U,s,V.conj()

# Problem 2
def visualize_svd(A):
    """Plot the effect of the SVD of A as a sequence of linear transformations
    on the unit circle and the two standard basis vectors.
    """
    theta=np.linspace(0,2*np.pi,200)
    x=np.cos(theta)
    y=np.sin(theta)
    S=np.vstack((x,y))
    E=np.array([[1,0,0],[0,0,1]])
    U,Sigma,VH=la.svd(A)
    Sigma=np.diag(Sigma)

    p1=plt.subplot(221)
    p1.plot(S[0],S[1])
    p1.plot(E[0],E[1])
    p1.axis("equal")

    p2=plt.subplot(222)
    p2.plot((VH@S)[0],(VH@S)[1])
    p2.plot((VH@E)[0],(VH@E)[1])
    p2.axis("equal")

    p3=plt.subplot(223)
    p3.plot((Sigma@VH@S)[0],(Sigma@VH@S)[1])
    p3.plot((Sigma@VH@E)[0],(Sigma@VH@E)[1])
    p3.axis("equal")

    p4=plt.subplot(224)
    p4.plot((U@Sigma@VH@S)[0],(U@Sigma@VH@S)[1])
    p4.plot((U@Sigma@VH@E)[0],(U@Sigma@VH@E)[1])
    p4.axis("equal")

    plt.show()

# Problem 3
def svd_approx(A, s):
    """Return the best rank s approximation to A with respect to the 2-norm
    and the Frobenius norm, along with the number of bytes needed to store
    the approximation via the truncated SVD.

    Parameters:
        A ((m,n), ndarray)
        s (int): The rank of the desired approximation.

    Returns:
        ((m,n), ndarray) The best rank s approximation of A.
        (int) The number of entries needed to store the truncated SVD.
    """
    if s>np.linalg.matrix_rank(A):
        raise ValueError("s must be less than or equal to rank(A)")
    m,n=A.shape
    #U,S,VH=compact_svd(A)
    U,S,VH=la.svd(A)
    S=np.diag(S)
    return U[:,:s]@S[:s,:s]@VH[:s],m*s+s+s*n

# Problem 4
def lowest_rank_approx(A, err):
    """Return the lowest rank approximation of A with error less than 'err'
    with respect to the matrix 2-norm, along with the number of bytes needed
    to store the approximation via the truncated SVD.

    Parameters:
        A ((m, n) ndarray)
        err (float): Desired maximum error.

    Returns:
        A_s ((m,n) ndarray) The lowest rank approximation of A satisfying
            ||A - A_s||_2 < err.
        (int) The number of entries needed to store the truncated SVD.
    """
    Sigma=compact_svd(A)[1]
    if err<=Sigma[len(Sigma)-1]:
        raise ValueError("err must be greater than the smallest singular value of A")
    s=0
    for i in range(len(Sigma)-1):
        if Sigma[i+1]<err:
            s=i
            break
    return svd_approx(A,s)

# Problem 5
def compress_image(filename, s):
    """Plot the original image found at 'filename' and the rank s approximation
    of the image found at 'filename.' State in the figure title the difference
    in the number of entries used to store the original image and the
    approximation.

    Parameters:
        filename (str): Image file path.
        s (int): Rank of new image.
    """
    image1=imread(filename)/255
    image2=np.copy(image1)
    if len(image1.shape)==2:
        image2=svd_approx(image1,s)[0]
    else:
        R=svd_approx(image1[:,:,0],s)[0]
        G=svd_approx(image1[:,:,1],s)[0]
        B=svd_approx(image1[:,:,2],s)[0]
        image2=np.dstack((R,G,B))

    image2=np.clip(image2,0,1)
    img1=plt.subplot(121)
    img1.imshow(image1,cmap="gray")
    img1.axis("off")

    img2=plt.subplot(122)
    img2.imshow(image2,cmap="gray")
    img2.axis("off")

    plt.show()
