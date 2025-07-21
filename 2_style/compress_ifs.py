# STYLE ***************************************************************************
# content = assignment (Python Advanced)
#
# date    = 2025-03-07
# email   = contact@alexanderrichtertd.com
#**********************************************************************************


# Change color of controls in Maya

def set_color(ctrlList=None, color=None):
    if not ctrlList or color is None:
        return

    color_map = {
        1: 4,
        2: 13,
        3: 25,
        4: 17,
        5: 17,
        6: 15,
        7: 6,
        8: 16
    }
    
    override_color = color_map.get(color)
    if override_color is None:
        return
    
    for ctrlName in ctrlList:
        shape_name = ctrlName + 'Shape'
        try:
            mc.setAttr(shape_name + '.overrideEnabled', 1)
            mc.setAttr(shape_name + '.overrideColor', override_color)
        except:
            pass 



