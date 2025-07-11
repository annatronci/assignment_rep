# 07 Week *********************************************************************
# content = test usersetup
#
# date    = 2024-05-06
# author  = contact@alexanderrichtertd.com
#******************************************************************************


import hou


def check_startup():
    obj = hou.node('obj')
    geo = obj.createNode('geo')
    box = geo.createNode('box')
    print('Now you can start to work!')
