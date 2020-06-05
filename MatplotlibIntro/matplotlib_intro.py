# matplotlib_intro.py
"""Python Essentials: Intro to Matplotlib.
Nathan Kibanoff
BUDS Training Program
30 July 2019
"""
import numpy as np
from matplotlib import pyplot as plt
# Problem 1
def var_of_means(n):
    """Construct a random matrix A with values drawn from the standard normal
    distribution. Calculate the mean value of each row, then calculate the
    variance of these means. Return the variance.

    Parameters:
        n (int): The number of rows and columns in the matrix A.

    Returns:
        (float) The variance of the means of each row.
    """
    normal=np.random.normal(size=(n,n))
    means=np.mean(normal,axis=1)
    return np.var(means)

def prob1():
    """Create an array of the results of var_of_means() with inputs
    n = 100, 200, ..., 1000. Plot and show the resulting array.
    """
    vars=[]
    for i in range(1,11):
        vars.append(var_of_means(i*100))
    vars=np.array(vars)
    plt.plot(100*np.arange(1,11),vars)
    plt.show()

# Problem 2
def prob2():
    """Plot the functions sin(x), cos(x), and arctan(x) on the domain
    [-2pi, 2pi]. Make sure the domain is refined enough to produce a figure
    with good resolution.
    """
    x=np.linspace(-2*np.pi,2*np.pi)
    sine=np.sin(x)
    cosine=np.cos(x)
    atan=np.arctan(x)
    plt.plot(x,sine,label="y = sin(x)")
    #plt.show()
    plt.plot(x,cosine,label="y = cos(x)")
    #plt.show()
    plt.plot(x,atan,label="y = arctan(x)")
    plt.legend()
    plt.show()

# Problem 3
def prob3():
    """Plot the curve f(x) = 1/(x-1) on the domain [-2,6].
        1. Split the domain so that the curve looks discontinuous.
        2. Plot both curves with a thick, dashed magenta line.
        3. Set the range of the x-axis to [-2,6] and the range of the
           y-axis to [-6,6].
    """
    x=np.linspace(-2,6,65)
    f=1/(x-1)
    plt.plot(x,f,"m--",lw=4)
    plt.plot(x[:23],f[:23],"m--",lw=4)
    plt.plot(x[25:],f[25:],"m--",lw=4)
    plt.xlim(-2,6)
    plt.ylim(-6,6)
    plt.show()

# Problem 4
def prob4():
    """Plot the functions sin(x), sin(2x), 2sin(x), and 2sin(2x) on the
    domain [0, 2pi].
        1. Arrange the plots in a square grid of four subplots.
        2. Set the limits of each subplot to [0, 2pi]x[-2, 2].
        3. Give each subplot an appropriate title.
        4. Give the overall figure a title.
        5. Use the following line colors and styles.
              sin(x): green solid line.
             sin(2x): red dashed line.
             2sin(x): blue dashed line.
            2sin(2x): magenta dotted line.
    """
    x=np.linspace(0,2*np.pi)
    sinx=np.sin(x)
    sin2x=np.sin(2*x)
    tsinx=2*sinx
    tsin2x=2*sin2x

    p1=plt.subplot(221)
    p1.set_title("y = sin(x)")
    p1.plot(x,sinx,"g-")
    p1.axis([0,2*np.pi,-2,2])

    p2=plt.subplot(222)
    p2.set_title("y = sin(2x)")
    p2.plot(x,sin2x,"r--")
    p2.axis([0,2*np.pi,-2,2])

    p3=plt.subplot(223)
    p3.set_title("y = 2sin(x)")
    p3.plot(x,tsinx,"b--")
    p3.axis([0,2*np.pi,-2,2])

    p4=plt.subplot(224)
    p4.set_title("y = 2sin(2x)")
    p4.plot(x,tsin2x,"m:")
    p4.axis([0,2*np.pi,-2,2])

    plt.suptitle("Frequency and amplitude of the sine function")
    plt.show()

# Problem 5
def prob5():
    """Visualize the data in FARS.npy. Use np.load() to load the data, then
    create a single figure with two subplots:
        1. A scatter plot of longitudes against latitudes. Because of the
            large number of data points, use black pixel markers (use "k,"
            as the third argument to plt.plot()). Label both axes.
        2. A histogram of the hours of the day, with one bin per hour.
            Label and set the limits of the x-axis.
    """
    fars=np.load("FARS.npy")

    p1=plt.subplot(121)
    p1.plot(fars.T[1],fars.T[2],"k,")
    p1.set_xlabel("Longitude")
    p1.set_ylabel("Latitude")
    p1.set_aspect("equal")

    p2=plt.subplot(122)
    p2.hist(fars.T[0],bins=np.arange(0,25))
    p2.set_xlabel("Hour")
    plt.xlim(0,24)

    plt.show()

# Problem 6
def prob6():
    """Plot the function f(x,y) = sin(x)sin(y)/xy on the domain
    [-2pi, 2pi]x[-2pi, 2pi].
        1. Create 2 subplots: one with a heat map of f, and one with a contour
            map of f. Choose an appropriate number of level curves, or specify
            the curves yourself.
        2. Set the limits of each subplot to [-2pi, 2pi]x[-2pi, 2pi].
        3. Choose a non-default color scheme.
        4. Add a colorbar to each subplot.
    """
    x=np.linspace(-2*np.pi,2*np.pi)
    y=x.copy()
    x1,y1=np.meshgrid(x,y)
    f=np.sin(x1)*np.sin(y1)/(x1*y1)

    plt.subplot(121)
    plt.pcolormesh(x1,y1,f,cmap="magma")
    plt.colorbar()
    plt.axis([-2*np.pi,2*np.pi,-2*np.pi,2*np.pi])

    plt.subplot(122)
    plt.contour(x1,y1,f,10,cmap="coolwarm")
    plt.colorbar()
    plt.axis([-2*np.pi,2*np.pi,-2*np.pi,2*np.pi])

    plt.show()
