# ADVANCED ***************************************************************************
# content = assignment
#
# date    = 2022-01-07
# email   = contact@alexanderrichtertd.com
#************************************************************************************

"""
CUBE CLASS

1. CREATE an abstract class "Cube" with the functions:
   translate(x, y, z), rotate(x, y, z), scale(x, y, z) and color(R, G, B)
   All functions store and print out the data in the cube (translate, rotate, scale and color).

2. ADD an __init__(name) and create 3 cube objects.

3. ADD the function print_status() which prints all the variables nicely formatted.

4. ADD the function update_transform(ttype, value).
   "ttype" can be "translate", "rotate" and "scale" while "value" is a list of 3 floats.
   This function should trigger either the translate, rotate or scale function.

   BONUS: Can you do it without using ifs?

5. CREATE a parent class "Object" which has a name, translate, rotate and scale.
   Use Object as the parent for your Cube class.
   Update the Cube class to not repeat the content of Object.

"""

from abc import ABC, abstractmethod


class Object:
    def __init__(self, name):
        self.name = name
        self.translation = [0.0, 0.0, 0.0]
        self.rotation = [0.0, 0.0, 0.0]
        self.scaling = [1.0, 1.0, 1.0]

    def translate(self, x, y, z):
        self.translation = [x, y, z]
        print(f"[{self.name}] Translate set to {self.translation}")

    def rotate(self, x, y, z):
        self.rotation = [x, y, z]
        print(f"[{self.name}] Rotate set to {self.rotation}")

    def scale(self, x, y, z):
        self.scaling = [x, y, z]
        print(f"[{self.name}] Scale set to {self.scaling}")



class Cube(Object, ABC):
    def color(self, R, G, B):
        pass 


class MyCube(Cube):
    def __init__(self, name, R=1.0, G=1.0, B=1.0):
        super().__init__(name)
        self.color(R, G, B)

    def color(self, R, G, B):
        self.color_value = [R, G, B]
        print(f"[{self.name}] Color set to {self.color_value}")

    def print_status(self):
        print(f"\n=== {self.name} STATUS ===")
        print(f"Translate: {self.translation}")
        print(f"Rotate: {self.rotation}")
        print(f"Scale: {self.scaling}")
        print(f"Color: {self.color_value}")

    def update_transform(self, ttype, value):
        getattr(self, ttype)(*value)  # senza if



if __name__ == "__main__":
    cube1 = MyCube("Cube 1", 1.0, 0.0, 0.0)
    cube2 = MyCube("Cube 2", 0.0, 1.0, 0.0)
    cube3 = MyCube("Cube 3", 0.0, 0.0, 1.0)

    
    cube1.translate(1, 2, 3)
    cube2.rotate(45, 0, 90)
    cube3.scale(2, 2, 2)


    cube1.update_transform("translate", [10, 10, 10])
    cube2.update_transform("rotate", [0, 45, 0])
    cube3.update_transform("scale", [0.5, 0.5, 0.5])

    
    cube1.print_status()
    cube2.print_status()
    cube3.print_status()

    

