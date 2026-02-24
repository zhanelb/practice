#1
import math
degree = float(input("Input degree: "))
radian=math.radians(degree)
print("Output radian:", round(radian, 6))
#2
import math
height=int(input("Height: "))
base1=int(input("Base, first value: "))
base2=int(input("Base, second value: "))
area=(base1+base2)/2*height
print("Expected Output: ",area)
#3
import math
n=int(input("Input number of sides: "))
s=int(input("Input the length of a side: "))
area=(n*s*s)/(4*math.tan(math.pi/n))
print("The area of the polygon is: ",round(area))
#4
import math
n=float(input("Length of base: "))
s=float(input("Height of parallelogram: "))
area=n*s
print("Expected Output: ",area)