# standard_library.py
"""Python Essentials: The Standard Library.
Nathan John L. Kibanoff
BUDS Training Program
12 July 2019
"""
import calculator as calc
import itertools as it
import box
import sys
import random
import time

# Problem 1
def prob1(L):
    """Return the minimum, maximum, and average of the entries of L
    (in that order).
    """
    return (min(L),max(L),sum(L)/len(L))
    raise NotImplementedError("Problem 1 Incomplete")

# Problem 2
def prob2():
    """Determine which Python objects are mutable and which are immutable.
    Test numbers, strings, lists, tuples, and sets. Print your results.
    """
    int1=1
    int2=int1
    int2+=1
    if int1==int2:
        print("numbers are mutable")
    else:
        print("numbers are not mutable")

    str1="str1"
    str2=str1
    str2="str2"
    if str1==str2:
        print("strings are mutable")
    else:
        print("strings are not mutable")

    list1=[1,2]
    list2=list1
    list2[0]=3
    if list1==list2:
        print("lists are mutable")
    else:
        print("lists are not mutable")

    tuple1=("tuple",1)
    tuple2=tuple1
    tuple2+=(1,)
    if tuple1==tuple2:
        print("tuples are mutable")
    else:
        print("tuples are not mutable")

    set1={"set","theory"}
    set2=set1
    set2.add("string theory")
    if set1==set2:
        print("sets are mutable")
    else:
        print("sets are not mutable")
    return

    raise NotImplementedError("Problem 2 Incomplete")

# Problem 3
def hypot(a, b):
    """Calculate and return the length of the hypotenuse of a right triangle.
    Do not use any functions other than those that are imported from your
    'calculator' module.

    Parameters:
        a: the length one of the sides of the triangle.
        b: the length the other non-hypotenuse side of the triangle.
    Returns:
        The length of the triangle's hypotenuse.
    """
    return calc.math.sqrt(calc.sum(calc.product(a,a),calc.product(b,b)))
    raise NotImplementedError("Problem 3 Incomplete")

# Problem 4
def power_set(A):
    """Use itertools to compute the power set of A.

    Parameters:
        A (iterable): a str, list, set, tuple, or other iterable collection.

    Returns:
        (list(sets)): The power set of A as a list of sets.
    """
    pset=[]
    for i in range(len(A)+1):
        pset+=list(it.combinations(A,i))
    for i in range(len(pset)):
        pset[i]=set(pset[i])
    return pset
    raise NotImplementedError("Problem 4 Incomplete")

# Problem 5: Implement shut the box.
def shutTheBox(name,seconds):
    if seconds<=0:
        print("Number of seconds must be greater than zero")
        return
    rem=[1,2,3,4,5,6,7,8,9]
    roll=0
    total_time=0
    if sum(rem)>6:
        roll=random.randint(2,12)
    else:
        roll=random.randint(1,6)
    print("Numbers left:",rem)
    print("Roll:",roll)
    while total_time<seconds and box.isvalid(roll,rem) and rem!=[]:
        print("Seconds left:",round(seconds-total_time,2))
        start=time.time()
        elim=input("Numbers to eliminate: ")
        end=time.time()
        total_time+=end-start
        elim=box.parse_input(elim,rem)
        if sum(elim)!=roll:
            print("Invalid input\n")
            continue
        for i in range(len(elim)):
            rem.remove(elim[i])
        if sum(rem)>6:
            roll=random.randint(2,12)
        else:
            roll=random.randint(1,6)
        print()
        if total_time<seconds:
            print("Numbers left:",rem)
            print("Roll:",roll)
    if rem!=[]:
        print("Game over!")
    print("\nScore for player",name,"=",sum(rem))
    print("Time played:",round(total_time,2),"seconds")
    if rem==[]:
        print("Congratulations! You shut the box!")
    else:
        print("Better luck next time! >:)")

if len(sys.argv)==3:
    try:
        shutTheBox(sys.argv[1],float(sys.argv[2]))
    except ValueError:
        print("Third argument must be a number")
