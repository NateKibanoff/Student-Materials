# python_intro.py
"""Python Essentials: Introduction to Python.
Nathan John L. Kibanoff
BUDS Training Program
12 July 2019
"""
if __name__ == "__main__":
    print("Hello, world!")

def sphere_volume(r):
    """Returns the volume of a sphere with radius r."""
    return 4*3.14159*(r**3)/3

def isolate(a,b,c,d,e):
    """Takes five parameters and prints the first three parameters five spaces
    apart from each other. It then prints the remaining elements with one space
    from each other."""
    print(a,"   ",b,"   ",c,d,e)

def first_half(a):
    """Returns the first half of a string. If the string has an odd length, the
    function returns all characters before the middle character."""
    return a[0:len(a)//2]

def backward(a):
    """Reverses a given string."""
    back=""
    for i in range(len(a)-1,-1,-1):
        back+=a[i]
    return back

def list_ops():
    """Follows the set of instructions given for Problem 5 in the Python
    Introduction section."""
    ops=["bear","ant","cat","dog"]
    ops.append("eagle")
    ops[2]="fox"
    ops.remove(ops[1])
    ops.sort(reverse=True)
    ops[ops.index("eagle")]="hawk"
    ops[len(ops)-1]+="hunter"
    return ops

def pig_latin(word):
    """Translates a given word into Pig Latin."""
    vowels={"a","e","i","o","u"}
    if word[0] in vowels:
        return word+"hay"
    word+=word[0]+"ay"
    return word[1:]

def palindrome():
    """Computes for the largest palindromic number that can be expressed as
    the product of two three-digit integers."""
    largest=0
    for i in range(100,1000):
        for j in range(i,1000):
            if str(i*j)==backward(str(i*j)):
                largest=max(i*j,largest)
    return largest

def alt_harmonic(n):
    """Returns the nth element of a harmonic series."""
    harmonic=[1]
    for i in range(2,n+1):
        harmonic.append((-1)**(i+1)/i+harmonic[i-2])
    return harmonic[n-1]
