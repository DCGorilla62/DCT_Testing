from test_hv_conversions import *

CatV=3408.06
PotV=2192.29
CatVADC=CatV/conv_factor_HV
PotVADC=PotV/conv_factor_HV
newCatV=CatVADC*new_conv_factor_HVcat
newPotV=PotVADC*new_conv_factor_HVpot
print(f'CatV, {CatV} | CatVADC, {CatVADC} | CatV new, {newCatV}')
print(f'PotV, {PotV} | PotVADC, {PotVADC} | PotV new, {newPotV}')
