#include <iostream>
#include <cmath>
#include <stdint.h>
using namespace std;

/*
    hvmonconverted.CatV=hvmon.CatVmon*conv_factor_HV;
    hvmonconverted.CatI=hvmon.CatImon*conv_factor_current; // in mA instead
    hvmonconverted.PotV=hvmon.PotVmon*conv_factor_HV;
    hvmonconverted.PotI=hvmon.PotImon*conv_factor_current; // in mA
    memcpy(outbuffer, (uint8_t *) &hvmonconverted,sizeof(sDCTHVConverted));
    // now the controls, converted using full_inverted_conversion function
    hvcontrolconverted.CatV=full_inverted_conversion(voltage_cathode, highvolt_FS, cathode_scale_factor, cathode_volt_FS);
    hvcontrolconverted.CatI=full_inverted_conversion(current_cathode, highcurrent_FS, cathode_scale_factor,cathode_current_FS); // in uA instead
    hvcontrolconverted.PotV=full_inverted_conversion(voltage_potential, highvolt_FS, potential_voltage_scale_factor,potential_volt_FS);
    hvcontrolconverted.PotI=full_inverted_conversion(current_potential, highcurrent_FS, potential_current_scale_factor, potential_current_FS); // in uA
*/
const double cathode_scale_factor=1.13;
const double potential_voltage_scale_factor=1.0/2.21;
const double potential_current_scale_factor=1.0/13.0;
const double max_pin=4.64;
const double highvolt_FS=10000.0;  // in volts
const double highcurrent_FS=1500.0; // in microamps
const double cathode_volt_FS=9975.0; // in volts
const double cathode_current_FS=1496.0; // in microamps
const double potential_volt_FS=3994.0; // in volts
const double potential_current_FS=102.0; // in microamps
const float conversion_factor=3.3*1406.0/(1000.0*4096.0); // each ADC has a voltage divider and is 12-bits (3.3V FSR) so thats these numbers.
const float conv_factor_HV=conversion_factor*(10000.0/4.64); // now in volts, HV line value
const float conv_factor_current=conversion_factor*(1.5/4.64); // in milliAmps
const float new_conv_factor_HVcat=conversion_factor*(cathode_volt_FS/4.096); // now in volts, HV line value
const float new_conv_factor_HVpot=conversion_factor*(potential_volt_FS/4.096); // now in volts, HV line value


struct sDCTHV {
  uint16_t CatVmon; // 12 bits ADC, Cathode HV supply Vmon
  uint16_t CatImon; // 12 bits ADC, Cathode HV supply Imon
  uint16_t PotVmon; // 12 bits ADC, Potential HV supply Vmon
  uint16_t PotImon; // 12 bits ADC, Potential HV supply Imon
} __attribute__((packed));

// structs for testing code like ucontroller
struct sDCTHVConverted {
  float CatV; // 12 bits ADC converted to Volts-Cathode HV supply
  float CatI; // 12 bits ADC, converted to mA-Cathode HV supply
  float PotV; // 12 bits ADC, converted to Volts-Potential HV supply
  float PotI; // 12 bits ADC, converted to mA-Potential HV supply
} __attribute__((packed));

// required conversions
float convert_daccode_to_vout(uint16_t input){
  return (input*4.096/4096.0);
}

float convert_vout_to_vprog(float input,double fs){
  return (input*fs);
}

float convert_vprog_to_supply(float input,float FS){
  return (input*FS/max_pin);
}
// required inversions
int convert_vout_to_daccode(float input){
  return lround(input*4096.0/4.096);
}

float convert_vprog_to_vout(float input,float fs){
  return (input/fs);
}

float convert_supply_to_vprog(float input,float FS){
  return (input*4.64/FS);
}

float full_inverted_conversion(uint16_t write_val, float FS_X, float fs_x, float max_in){
  if(write_val<=4095){
    float vout_DAC=convert_daccode_to_vout(write_val);
    float voltage_on_programming_pin=convert_vout_to_vprog(vout_DAC,fs_x);
    float vsupply_val=convert_vprog_to_supply(voltage_on_programming_pin,FS_X);
    if(vsupply_val<=max_in) return (vsupply_val);
  }
  else return 0;
}

uint16_t full_conversion(double write_val_d, double FS_X, double fs_x, double max_in){
  if(write_val_d<=max_in){
    double voltage_on_programming_pin=convert_supply_to_vprog(write_val_d,FS_X);
    //Serial.println(voltage_on_programming_pin,4);
    double vout_DAC=convert_vprog_to_vout(voltage_on_programming_pin,fs_x);
    //Serial.println(vout_DAC,4);
    long int to_write_code=convert_vout_to_daccode(vout_DAC);
    //Serial.println(to_write_code);
    if(to_write_code<=4096) return ((uint16_t)(to_write_code));
  }
  else return 0;
}

int main(){
 
  sDCTHV hvmon;
  sDCTHVConverted hvmonconverted;
  sDCTHVConverted hvcontrolconverted;
  hvmonconverted.CatV=3408.06;
  hvmonconverted.PotV=2192.29;
  hvmon.CatVmon= (uint16_t) lround(hvmonconverted.CatV/conv_factor_HV);
  hvmon.PotVmon= (uint16_t) lround(hvmonconverted.PotV/conv_factor_HV);

//  hvmonconverted.PotV=366.20;

//  uint16_t catV_adc= full_conversion(hvmonconverted.CatV, highvolt_FS, cathode_scale_factor,cathode_volt_FS);
//  uint16_t potV_adc= full_conversion(hvmonconverted.PotV, highvolt_FS, potential_voltage_scale_factor,potential_volt_FS);
  // now convert to new values, where its out of 4.096 not out of 4.64
  float new_catV= (float) (hvmon.CatVmon) * new_conv_factor_HVcat;
  float new_potV= (float) (hvmon.PotVmon) * new_conv_factor_HVpot;

// print them all
  cout << "CatV, CatV ADC, CatV new, PotV, PotV ADC, PotV new" << endl;
  cout << hvmonconverted.CatV << ", " << (int) hvmon.CatVmon << ", " << new_catV << ", " << (float) hvmonconverted.PotV << ", " << (int) hvmon.PotVmon << ", " << new_potV << endl;
  return 0;
}

