# exceptions_fileIO.py
"""Python Essentials: Exceptions and File Input/Output.
Nathan Kibanoff
BUDS Training Program
31 July 2019
"""

from random import choice

def isReverse(a,b):
    """Check if two strings are reversed versions of each other.

    Parameters:
        a, b (str): The two strings that will be compared with each other.

    Returns:
        (bool) True if a and b are reversed versions of each other.
        Otherwise, False
    """
    a,b=str(a),str(b)
    if len(a)!=len(b):
        return False
    for i in range(len(a)//2):
        if a[i]!=b[len(b)-1-i]:
            return False
    return True

# Problem 1
def arithmagic():
    """Prompts the user to enter four numbers in the following order: a
    three-digit number whose first and last digits differ by at least two, its
    reverse, the positive difference of the previous two numbers, and its
    reverse. The sum of the third and fourth numbers should be equal to 1089.
    If the user fails to follow any of the instructions, a ValueError would be
    raised with an appropriate error message.
    """
    step_1 = input("Enter a 3-digit number where the first and last "
                                           "digits differ by 2 or more: ")
    if len(step_1)!=3:
        raise ValueError("That is not a 3-digit number")
    if abs(int(step_1[0])-int(step_1[2]))<2:
        raise ValueError("The first number’s first and last digits differ by less than 2")
    step_2 = input("Enter the reverse of the first number, obtained "
                                              "by reading it backwards: ")
    if not isReverse(step_1,step_2):
        raise ValueError("That is not the reverse of the first number")
    step_3 = input("Enter the positive difference of these numbers: ")
    if abs(int(step_1)-int(step_2))!=int(step_3):
        raise ValueError("That is not the positive difference of the previous two numbers")
    step_4 = input("Enter the reverse of the previous result: ")
    if not isReverse(step_3,step_4):
        raise ValueError("That is not the reverse of the third number")
    print(str(step_3), "+", str(step_4), "= 1089 (ta-da!)")

# Problem 2
def random_walk(max_iters=1e12):
    """This function simulates a path created by a sequence of random steps by
    repeatedly adding or subtracting 1 to a running total. If the user
    interrupts the program while it's running, this method will catch the
    exception and print the iteration where the user interrupted.

    Parameters:
        max_iters (float): Maximum number of iterations for this function, with
            a default value of 1e12

    Returns:
        (int) The running total after randomly adding and subtracting 1.
    """
    walk = 0
    directions = [1, -1]
    for i in range(int(max_iters)):
        try:
            walk += choice(directions)
        except KeyboardInterrupt:
            print("Process interrupted at iteration",i)
            return walk
    print("Process completed")
    return walk
    
# Problems 3 and 4: Write a 'ContentFilter' class.
class ContentFilter:
    """A ContentFilter object class. Reads a file and stores its contents and
    details on its characters and lines.

    Attributes:
        name (str): filename of the file to be read
        contents (str): contents of the file
        total (int): total number of characters
        alphabetic (int): number of alphabetic characters
        numerical (int): number of numerical characters
        whitespace (int): number of whitespace characters
        lines (int): number of lines
    """
    def __init__(self,filename):
        """Set the name, contents, and details of the given file. If the input
        file doesn't exist, the constructor will prompt the user to enter an
        existing filename.

        Parameters:
            filename (str): Filename of the input file
        """
        try:
            file=open(filename,"r")
            self.name=filename
            self.contents=file.read()
            self.total=len(self.contents)
            self.alphabetic=0
            self.numerical=0
            lines=self.contents.split("\n")
            self.whitespace=len(lines)
            if lines[-1]=="":
                self.whitespace-=1
            self.lines=len(lines)
            for i in range(len(lines)):
                for j in range(len(lines[i])):
                    if lines[i][j].isalpha():
                        self.alphabetic+=1
                    elif lines[i][j].isdigit():
                        self.numerical+=1
                    elif lines[i][j].isspace():
                        self.whitespace+=1
            file.close()
        except (FileNotFoundError,TypeError,OSError):
            cf=ContentFilter(input("Please enter a valid file name: "))
            # 'self = cf' doesn't work :(
            self.name=cf.name
            self.contents=cf.contents
            self.total=cf.total
            self.alphabetic=cf.alphabetic
            self.numerical=cf.numerical
            self.whitespace=cf.whitespace
            self.lines=cf.lines
    def uniform(self,filename,mode="w",case="upper"):
        """Sets the contents of the source file into upper/lowercase characters
        and prints the result onto an output file.

        Parameters:
            filename (str): Name of the output file.
            mode (str): Modes for writing onto the output file. Only takes the
                values 'w' (default), 'x' or 'a'. Raises a ValueError otherwise.
            case (str): Determines if the output file should contain uppercase
                (default) or lowercase characters. Only takes the values "upper"
                and "lower". Raises a ValueError otherwise.
        """
        if mode not in ("w","x","a"):
            raise ValueError("attribute mode should either be 'w', 'x', or 'a'")
        if case not in ("upper","lower"):
            raise ValueError("attribute case should either be \"upper\" or \"lower\"")
        with open(filename,mode) as out:
            if case=="upper":
                out.write(self.contents.upper())
            elif case=="lower":
                out.write(self.contents.lower())
    def reverse(self,filename,mode="w",unit="line"):
        """Reverses the contents of the source file (either reverse the order of
        the lines or the order of the words per line) and prints the result onto
        an output file.

        Parameters:
            filename (str): Name of the output file.
            mode (str): Modes for writing onto the output file. Only takes the
                values 'w' (default), 'x' or 'a'. Raises a ValueError otherwise.
            unit (str): Determines how the contents of the source file should be
                reversed. If the value of unit is "line" (default), this method
                will reverse the order of the lines. If the value is "word",
                then this will reverse the order of the words for each line
                instead. This function raises a ValueError for other values of
                unit.
        """
        if mode not in ("w","x","a"):
            raise ValueError("attribute mode should either be 'w', 'x', or 'a'")
        if unit not in ("line","word"):
            raise ValueError("attribute unit should either be \"line\" or \"word\"")
        with open(filename,mode) as out:
            lines=self.contents.split("\n")
            if unit=="line":
                for i in range(len(lines)-1,-1,-1):
                    out.write(lines[i]+"\n")
            elif unit=="word":
                for i in range(len(lines)):
                    words=lines[i].split(" ")
                    for j in range(len(words)-1,-1,-1):
                        out.write(words[j]+" ")
                    out.write("\n")
    def transpose(self,filename,mode="w"):
        """Transposes the contents of the source file and prints the result onto
        an output file. (i.e. The ith word of the jth line in the source file
        will be printed as the jth word of the ith line on the output file)

        Parameters:
            filename (str): Name of the output file.
            mode (str): Modes for writing onto the output file. Only takes the
                values 'w' (default), 'x' or 'a'. Raises a ValueError otherwise.
        """
        if mode not in ("w","x","a"):
            raise ValueError("attribute mode should either be 'w', 'x', or 'a'")
        with open(filename,mode) as out:
            lines=self.contents.split("\n")
            words=[]
            for i in range(len(lines)):
                words.append(lines[i].split(" "))
            if(len(words[-1])!=len(words[-2])):
                words.remove(words[-1])
            for i in range(len(words[0])):
                for j in range(len(words)):
                    out.write(words[j][i]+" ")
                out.write("\n")
    def __str__(self):
        """Returns a string representation of the ContentFilter object which
        shows the filename of the source file, its total number of characters,
        number of alphabetic, numerical, and whitespace characters, and number
        of lines.

        Returns:
            (string) String representation of the object with all the relevant
            details.
        """
        src="Source file:\t\t"+self.name+"\n"
        total="Total characters:\t"+str(self.total)+"\n"
        alpha="Alphabetic characters:\t"+str(self.alphabetic)+"\n"
        num="Numerical characters:\t"+str(self.numerical)+"\n"
        space="Whitespace characters:\t"+str(self.whitespace)+"\n"
        lines="Number of lines:\t"+str(self.lines)
        return src+total+alpha+num+space+lines
