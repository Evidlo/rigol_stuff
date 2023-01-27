# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 13:57:32 2013

@author: bjuluri
Uses Pyvisa for communication
"""

from usbtmc import usbtmc
import time

delay = 0.5

class Rigol():
    def __init__(self, serial, delay=0.1, debug=False):
        self.debug = debug
        if self.debug:
            print('device_str:', device_str)
        self.instrument = usbtmc.Instrument(self.find_usbtmc(serial))
        self.delay=delay

    def find_usbtmc(self, iSerial):
        """Find usbtmc device by serial"""
        for dev in usbtmc.list_devices():
            if dev.serial_number == iSerial:
                return dev
        else:
            raise Exception(f'Device with serial {iSerial} not found')

    def write(self, message):
        if self.debug:
            print(message)
        self.instrument.write(message)
        time.sleep(self.delay)
        error = self.instrument.ask('SYST:ERR?')
        if error[0]:
            pass
        else :
            print(message+' received. An Error occured: '+ str(error))

    def query(self, message):
        if self.debug:
            print(message)
        result = self.instrument.ask(message)
        time.sleep(self.delay)
        return result

    def reset(self):
        """resets the instrument, registers,buffers"""
        self.write("*RST")
        time.sleep(self.delay)

    def close(self):
        self.instrument.close()


class RigolDM3058(Rigol):
    def meas_voltage(self):
        return float(self.query(f':MEAS:VOLT:DC?'))

    def meas_current(self):
        return float(self.query(f':MEAS:CURR:DC?'))

    def reset(self):
        try:
            Rigol.reset()
        except Exception as e:
            if 'Operation timed out' in e.args[0]:
                pass
            else:
                raise e

class RigolDP821(Rigol):
    def turn_off(self, chan=1):
        self.write(f':OUTP CH{chan},OFF')

    def turn_on(self, chan=1):
        self.write(f':OUTP CH{chan},ON')

    def sel_output(self, chan=1):
        cmd1 = ':INST:NSEL %s' %chan
        self.write(cmd1)
        time.sleep(self.delay)

    def set_voltage(self, voltage, max_current=None, chan=1):
        self.write(f':INST:NSEL {chan}')
        self.write(f':VOLT {voltage}')
        if max_current is not None:
            self.set_ocp(max_current, chan)
            self.toggle_ocp('ON')
        else:
            self.toggle_ocp('OFF')

    def set_current(self, current, max_voltage=None, chan=1):
        self.write(f':INST:NSEL {chan}')
        self.write(f':CURR {current}')
        if max_voltage is not None:
            self.set_ovp(max_voltage, chan)
            self.toggle_ovp('ON')
        else:
            self.toggle_ovp('OFF')

    def set_ovp(self, max_voltage, chan=1):
        self.write(f':INST:NSEL {chan}')
        self.write(f':VOLT:PROT {max_voltage}')

    def toggle_ovp(self, state):
        self.write(f':VOLT:PROT:STAT {state}')

    def set_ocp(self, max_current, chan=1):
        self.write(f':INST:NSEL {chan}')
        self.write(f':CURR:PROT {max_current}')

    def toggle_ocp(self, state):
        self.write(f':CURR:PROT:STAT {state}')

    def meas_voltage(self, chan=1):
        return float(self.query(f':MEAS:VOLT? CH{chan}'))

    def meas_current(self, chan=1):
        return float(self.query(f':MEAS:CURR? CH{chan}'))

    def meas_power(self, chan=1):
        return float(self.query(f':MEAS:POWE? CH{chan}'))


if __name__ == "__main__":
    # get these from 'lsbusb -v'

    # power supply
    # dcps = RigolDP821(vendor="0x1ab1", product="0x0e11", serial="DP8G194400109")
    # r.reset()
    # r.set_voltage(voltage=v, max_current=0.5)
    # r.turn_on()
    # time.sleep(1)
    # r.turn_off()
    # r.close()

    # multimeter
    dm = RigolDM3058(vendor="0x1ab1", product="0x09c4", serial="DM3L223900431", debug=True)
    # dm.reset()
    # print(dm.meas_voltage())
    # print(dm.meas_current())
    # dm.close()
