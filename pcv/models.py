#
# Created on Wed Jul 27 2022
#
# Copyright (c) 2022 Your Company
#

mod_1 = """
# measurement model

lai_summer ~ lai_spring + t2m_winter +tp_winter
lai_spring ~ t2m_winter +tp_winter
"""

mod_2 = """
# measurement model

lai_summer ~ swvlall_summer + swvlall_winter + lai_spring + t2m_winter
swvlall_summer ~ lai_spring + swvlall_spring + t2m_summer+ tp_summer
lai_spring ~ swvlall_spring 
swvlall_spring ~ swvlall_winter + t2m_spring+ tp_spring
swvlall_winter ~ t2m_winter+ tp_winter

"""