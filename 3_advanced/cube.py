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

def print_value_edits(func):
    def decorator(*args, **kwargs):
        output = func(*args, **kwargs)
        transform_edit_result = 'Edited. {} : [ {}, {}, {}]'
        print(transform_edit_result.format(
            output[0], output[1], output[2], output[3]))
        
    return decorator

class Object:
    def __init__(self, name):
        self.name = name
        self._translate = [0, 0, 0]
        self._rotate = [0, 0, 0]
        self._scale = [1, 1, 1]

    @print_value_edits
    def translate(self, x, y, z):
        self.translate = [x, y, z]
        return ['translate', x, y, z]

    @print_value_edits
    def rotate(self, x, y, z):
        self.rotate = [x, y, z]
        return ['rotate', x, y, z]

    @print_value_edits
    def scale(self, x, y, z):
        self.scale = [x, y, z]
        return ['scale', x, y, z]

    def update_transform(self, ttype, value):
        transforms = {
            'translate': self.translate,
            'rotate': self.rotate,
            'scale': self.scale
        }
        transforms[ttype](value[0], value[1], value[2])



class Cube(Object):
    color_rgb = [0, 0, 0]

    @print_value_edits
    def color(self, r, g, b):
        self.color_rgb[0] = r
        self.color_rgb[1] = g
        self.color_rgb[2] = b
        return ['color', r, g, b]

    # create three instances

the_first_instance = Cube('myCube1')
the_second_instance = Cube('myCube2')
the_third_instance = Cube('myCube3')

# functionality test
print('Color')
print(the_first_instance.color(1, 2, 3))
the_second_instance.rotate(3, 2, 1)
the_third_instance.update_transform('scale', [12, 12, 12])

    

