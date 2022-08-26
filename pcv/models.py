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

# Model 3 lai lagged effect on soil moisture is considered
# Model also has all the climate 

mod_3 = """
# measurement model

lai_summer ~ lai_spring + swvlall_summer  + t2m_summer+ tp_summer
swvlall_summer ~ swvlall_spring + lai_spring  + t2m_summer+ tp_summer

lai_spring ~ lai_winter + swvlall_spring + t2m_spring+ tp_spring
swvlall_spring ~ swvlall_winter + lai_winter + t2m_spring+ tp_spring 

lai_winter ~ swvlall_winter + t2m_winter+ tp_winter 
swvlall_winter ~ t2m_winter+ tp_winter 
"""