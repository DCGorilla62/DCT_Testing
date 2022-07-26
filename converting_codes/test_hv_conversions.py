#hello

cathode_scale_factor=1.13;
potential_voltage_scale_factor=1.0/2.21;
potential_current_scale_factor=1.0/13.0;
max_pin=4.64;
highvolt_FS=10000.0;  # in volts
highcurrent_FS=1500.0; # in microamps
cathode_volt_FS=9975.0; # in volts
cathode_current_FS=1496.0; # in microamps
potential_volt_FS=3994.0; # in volts
potential_current_FS=102.0; # in microamps
conversion_factor=3.3*1406.0/(1000.0*4096.0); # each ADC has a voltage divider and is 12-bits (3.3V FSR) so thats these numbers.
conv_factor_HV=conversion_factor*(10000.0/4.64); # now in volts, HV line value
conv_factor_current=conversion_factor*(1.5/4.64); # in milliAmps
new_conv_factor_HVcat=conversion_factor*(cathode_volt_FS/4.096); # now in volts, HV line value
new_conv_factor_HVpot=conversion_factor*(potential_volt_FS/4.096); # now in volts, HV line value

# required conversions
def convert_daccode_to_vout(input):
      return (input*4.096/4096.0)

def convert_vout_to_vprog(input, fs):
      return (input*fs)

def convert_vprog_to_supply(input,FS):
      return (input*FS/max_pin)

def convert_vout_to_daccode(input):
      return int(input*4096.0/4.096)

def convert_vprog_to_vout(input,fs):
      return (input/fs)

def convert_supply_to_vprog(input,FS):
  return (input*4.64/FS)

def full_inverted_conversion(write_val,FS_X,fs_x,max_in):
      if write_val<=4095 :
            vout_DAC=convert_daccode_to_vout(write_val)
            voltage_on_programming_pin=convert_vout_to_vprog(vout_DAC,fs_x)
            vsupply_val=convert_vprog_to_supply(voltage_on_programming_pin,FS_X)
            if vsupply_val<=max_in:
                   return (vsupply_val)
      else:
            return 0

def full_conversion(write_val_d, FS_X, fs_x, max_in):
      if write_val_d<=max_in:
            voltage_on_programming_pin=convert_supply_to_vprog(write_val_d,FS_X)
            vout_DAC=convert_vprog_to_vout(voltage_on_programming_pin,fs_x)
            to_write_code=convert_vout_to_daccode(vout_DAC)
            if to_write_code<=4096:
                  return int(to_write_code)            
      else:
            return 0
