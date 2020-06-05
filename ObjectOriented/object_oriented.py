# object_oriented.py
"""Python Essentials: Object Oriented Programming.
Nathan Kibanoff
BUDS Training Program
17 July 2019
"""
import math
class Backpack:
    """A Backpack object class. Has a name and a list of contents.

    Attributes:
        name (str): the name of the backpack's owner.
        contents (list): the contents of the backpack.
        color (str): the color of the backpack.
        max_size (int): capacity of the backpack.
    """

    # Problem 1: Modify __init__() and put(), and write dump().
    def __init__(self, name, color, max_size=5):
        """Set the name, color, and maximum number of contents (default 5).

        Parameters:
            name (str): the name of the backpack's owner.
            color (str): the color of the backpack.
            max_size (int): capacity of the backpack with a default value of 5.
        """
        self.name = name
        self.contents = []
        self.color = color
        self.max_size = max_size

    def put(self, item):
        """Add an item to the backpack's list of contents if there is enough space."""
        if len(self.contents)<self.max_size:
            self.contents.append(item)
        else:
            print("No room!")

    def take(self, item):
        """Remove an item from the backpack's list of contents."""
        self.contents.remove(item)

    def dump(self):
        """Removes all the contents of the backpack."""
        self.contents = []

    # Magic Methods -----------------------------------------------------------

    # Problem 3: Write __eq__() and __str__().
    def __add__(self, other):
        """Add the number of contents of each Backpack."""
        return len(self.contents) + len(other.contents)

    def __lt__(self, other):
        """Compare two backpacks. If 'self' has fewer contents
        than 'other', return True. Otherwise, return False.
        """
        return len(self.contents) < len(other.contents)

    def __eq__(self,other):
        """Compare two backpacks. If 'self' and 'other' have the same name,
        color, and number of contents, return True. Otherwise, return False."""
        return self.name==other.name and self.color==other.color and len(self.contents)==len(other.contents)

    def __str__(self):
        """Returns a formatted string representation of the backpack object.
        It shows the backpack's owner, color, number of contents, capacity,
        and list of contents."""
        return "Owner:\t\t"+self.name+"\nColor:\t\t"+self.color+"\nSize:\t\t"+str(len(self.contents))+"\nMax Size:\t"+str(self.max_size)+"\nContents:\t"+str(self.contents)

# An example of inheritance. You are not required to modify this class.
class Knapsack(Backpack):
    """A Knapsack object class. Inherits from the Backpack class.
    A knapsack is smaller than a backpack and can be tied closed.

    Attributes:
        name (str): the name of the knapsack's owner.
        color (str): the color of the knapsack.
        max_size (int): the maximum number of items that can fit inside.
        contents (list): the contents of the backpack.
        closed (bool): whether or not the knapsack is tied shut.
    """
    def __init__(self, name, color):
        """Use the Backpack constructor to initialize the name, color,
        and max_size attributes. A knapsack only holds 3 item by default.

        Parameters:
            name (str): the name of the knapsack's owner.
            color (str): the color of the knapsack.
            max_size (int): the maximum number of items that can fit inside.
        """
        Backpack.__init__(self, name, color, max_size=3)
        self.closed = True

    def put(self, item):
        """If the knapsack is untied, use the Backpack.put() method."""
        if self.closed:
            print("I'm closed!")
        else:
            Backpack.put(self, item)

    def take(self, item):
        """If the knapsack is untied, use the Backpack.take() method."""
        if self.closed:
            print("I'm closed!")
        else:
            Backpack.take(self, item)

    def weight(self):
        """Calculate the weight of the knapsack by counting the length of the
        string representations of each item in the contents list.
        """
        return sum(len(str(item)) for item in self.contents)


# Problem 2: Write a 'Jetpack' class that inherits from the 'Backpack' class.
class Jetpack(Backpack):
    """A Jetpack object class that inherits from the Backpack class.

    Attributes:
        name (str): the name of the jetpack's owner.
        contents (list): the contents of the jetpack.
        color (str): the color of the jetpack.
        max_size (int): capacity of the jetpack.
        fuel (int): amount of fuel in the jetpack
    """
    def __init__(self,name,color,max_size=2,fuel=10):
        """Use the Jetpack constructor to initialize the name, color,
        and max_size attributes. A jetpack holds at most two items and 10 units
        of fuel by default.

        Parameters:
            name (str): the name of the knapsack's owner.
            color (str): the color of the knapsack.
            max_size (int): the maximum number of items that can fit inside.
        """
        Backpack.__init__(self,name,color,max_size)
        self.fuel=fuel
    def fly(self,fuel):
        """Consumes a given amount of fuel from the jetpck to make it fly."""
        if self.fuel-fuel>=0:
            self.fuel-=fuel
        else:
            print("Not enough fuel!")
    def dump(self):
        """Removes all the contents and fuel of the jetpack."""
        self.contents=[]
        self.fuel=0

# Problem 4: Write a 'ComplexNumber' class.
class ComplexNumber:
    """ComplexNumber object class. Has a real component and an imaginary component.

    Attributes:
        real (float): the real component of the complex number
        imag (float): the imaginary component of the complex number
    """

    def __init__(self,a,b):
        """Sets the real and imaginary parts of the complex number.

        Parameters:
            a (float): the real component of the complex number
            b (float): the imaginary component of the complex number
        """
        self.real=a
        self.imag=b
    def conjugate(self):
        """Returns the conjugate of the complex number by reversing the sign
        of the imaginary component."""
        return ComplexNumber(self.real,-self.imag)
    def __str__(self):
        """Returns the string representation of the complex number in the format
        '(a+bj)' or '(a-bj)' where a represents the real component and b
        represents the imaginary component."""
        if self.imag>=0:
            return "("+str(self.real)+"+"+str(self.imag)+"j)"
        return "("+str(self.real)+"-"+str(-self.imag)+"j)"
    def __abs__(self):
        """Returns the absolute value of the complex number by taking the square
        root of the sum of the squares of the real and imaginary components."""
        return math.sqrt(self.real**2+self.imag**2)
    def __eq__(self,other):
        """Compares two complex numbers. Returns True if the real
        and imaginary components of 'self' and 'other' are equal. Returns False
        otherwise."""
        return self.real==other.real and self.imag==other.imag
    def __add__(self,other):
        """Returns the sum of complex numbers 'self' and 'other'."""
        return ComplexNumber(self.real+other.real,self.imag+other.imag)
    def __sub__(self,other):
        """Returns the difference of complex numbers 'self' and 'other'."""
        return ComplexNumber(self.real-other.real,self.imag-other.imag)
    def __mul__(self,other):
        """Returns the product of complex numbers 'self' and 'other'."""
        real=self.real*other.real-self.imag*other.imag
        imag=self.real*other.imag+self.imag*other.real
        return ComplexNumber(real,imag)
    def __truediv__(self,other):
        """Returns the quotient of complex numbers 'self' and 'other'."""
        real=(self.real*other.real+self.imag*other.imag)/(other*other.conjugate()).real
        imag=(self.imag*other.real-self.real*other.imag)/(other*other.conjugate()).real
        return ComplexNumber(real,imag)

def test_ComplexNumber(a, b):
    """Tester function for the ComplexNumber class."""
    py_cnum, my_cnum = complex(a, b), ComplexNumber(a, b)
    # Validate the constructor.
    if my_cnum.real != a or my_cnum.imag != b:
        print("__init__() set self.real and self.imag incorrectly")
    # Validate conjugate() by checking the new number's imag attribute.
    if py_cnum.conjugate().imag != my_cnum.conjugate().imag:
        print("conjugate() failed for", py_cnum)
    # Validate __str__().
    if str(py_cnum) != str(my_cnum):
        print("__str__() failed for", py_cnum)
    # Validate __abs__()
    if abs(py_cnum)!=abs(my_cnum):
        print("__abs__() failed for",py_cnum)
    # Validate __eq__()
    if py_cnum!=my_cnum:
        print("__eq__() failed for",py_cnum)
    # Validate __add__()
    if py_cnum+py_cnum != my_cnum+my_cnum:
        print("__add__() failed for",py_cnum)
    # Validate __sub__()
    if py_cnum-py_cnum != my_cnum-my_cnum:
        print("__sub__() failed for",py_cnum)
    # Validate __mul__()
    if py_cnum*py_cnum != my_cnum*my_cnum:
        print("__mul__() failed for",py_cnum)
    # Validate __truediv__()
    if py_cnum/py_cnum != my_cnum/my_cnum:
        print("__truediv__() failed for",py_cnum)
