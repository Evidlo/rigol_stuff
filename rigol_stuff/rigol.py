# -*- coding: utf-8 -*-
"""
Reading USBTMC device in pure Python file IO
Evan Widloski - 2023-01-27
"""

import os
import time
from pathlib import Path

devpath = Path('/dev')

class Rigol():
    def __init__(self, serial, delay=0.1, debug=False):
        self.debug = debug
        if self.debug:
            print('device_str:', device_str)
        self.device_file = self.find_device(serial)
        self.delay=delay

    def find_device(self, serial):
        """Find usbtmc device by serial

        Args:
            serial (str): device iSerial string as shown in `lsusb -v`

        Returns:
            file_descriptor (int): Linux file descriptor to /dev/usbtmcX
        """
        for dev in devpath.glob('usbtmc*'):
            f = os.open(dev, os.O_RDWR)
            os.write(f, b'*IDN?\r\n')
            device_str = os.read(f, 1024).decode('ascii')
            if serial in device_str:
                return f
            else:
                os.close(f)
        else:
            raise Exception(f'Device with serial {serial} not found')

    def write(self, message):
        """Write a message to usbtmc device and check for error

        Args:
            message (str): usbtmc message to send to device
        """
        if self.debug:
            print(message)
        os.write(self.device_file, message.encode('ascii'))
        # os.read(self.device_file, 1024)
        # self.instrument.write(message)
        time.sleep(self.delay)
        # error = self.instrument.ask('SYST:ERR?')
        os.write(self.device_file, b'SYST:ERR?\r\n')
        code, msg = os.read(self.device_file, 1024).strip().split(b',')
        if code == b'0':
            pass
        else:
            print(f"Errno {code.decode('ascii')}: {msg.decode('ascii')}")

    def query(self, message):
        """Query usbtmc device for data

        Args:
            message (str): usbtmc query message

        Returns:
            result (str): response
        """
        if self.debug:
            print(message)
        os.write(self.device_file, message.encode('ascii'))
        time.sleep(self.delay)
        result = os.read(self.device_file, 1024).decode('ascii')
        # result = self.device.ask(message)
        return result

    def reset(self):
        """resets the instrument, registers,buffers"""
        self.write("*RST")

    def close(self):
        """Close the usbtmc file descriptor"""
        os.close(self.device_file)


class RigolDM3058(Rigol):
    def meas_voltage(self, mode='DC'):
        """Measure multimeter voltage"""
        return float(self.query(f':MEAS:VOLT:{MODE}?'))

    def meas_current(self, mode='DC'):
        """Measure multimeter current"""
        return float(self.query(f':MEAS:CURR:{MODE}?'))

    def reset(self):
        """Reset multimeter"""
        try:
            Rigol.reset(self)
        except Exception as e:
            if 'Connection timed out' in e.args[0]:
                pass
            else:
                raise e

class RigolDP821(Rigol):
    def turn_off(self, chan=1):
        """Turn off output channel

        Args:
            chan (int): channel number
        """
        self.write(f':OUTP CH{chan},OFF')

    def turn_on(self, chan=1):
        """Turn on output channel

        Args:
            chan (int): channel number
        """
        self.write(f':OUTP CH{chan},ON')

    def set_voltage(self, voltage, max_current=None, chan=1):
        """Set channel in constant voltage mode

        Args:
            voltage (float): channel voltage
            max_current (float or None): current limit
            chan (int): channel number
        """
        self.write(f':INST:NSEL {chan}')
        self.write(f':VOLT {voltage}')
        if max_current is not None:
            self.set_ocp(max_current, chan)
            self.toggle_ocp('ON')
        else:
            self.toggle_ocp('OFF')

    def set_current(self, current, max_voltage=None, chan=1):
        """Set channel in constant current mode

        Args:
            current (float): channel voltage
            max_voltage (float or None): voltage limit
            chan (int): channel number
        """
        self.write(f':INST:NSEL {chan}')
        self.write(f':CURR {current}')
        if max_voltage is not None:
            self.set_ovp(max_voltage, chan)
            self.toggle_ovp('ON')
        else:
            self.toggle_ovp('OFF')

    def set_ovp(self, max_voltage, chan=1):
        """Set voltage limit on channel

        Args:
            max_voltage (float or None): voltage limit
            chan (int): channel number
        """
        self.write(f':INST:NSEL {chan}')
        self.write(f':VOLT:PROT {max_voltage}')

    def set_ocp(self, max_current, chan=1):
        """Set channel in constant voltage mode

        Args:
            max_current (float or None): current limit
            chan (int): channel number
        """
        self.write(f':INST:NSEL {chan}')
        self.write(f':CURR:PROT {max_current}')

    def toggle_ovp(self, state, chan=1):
        """Enable/disable voltage limit

        Args:
            state (bool): voltage limit enabled
            chan (int): channel number
        """
        state = 'ON' if state else 'OFF'
        self.write(f':INST:NSEL {chan}')
        self.write(f':VOLT:PROT:STAT {state}')

    def toggle_ocp(self, state, chan=1):
        """Enable/disable current limit

        Args:
            state (bool): current limit enabled
            chan (int): channel number
        """
        state = 'ON' if state else 'OFF'
        self.write(f':INST:NSEL {chan}')
        self.write(f':CURR:PROT:STAT {state}')

    def meas_voltage(self, chan=1):
        """Measure channel voltage

        Args:
            chan (int): channel number

        Returns:
            voltage (float): channel voltage
        """
        return float(self.query(f':MEAS:VOLT? CH{chan}'))

    def meas_current(self, chan=1):
        """Measure channel current

        Args:
            chan (int): channel number

        Returns:
            current (float): channel current
        """
        return float(self.query(f':MEAS:CURR? CH{chan}'))

    def meas_power(self, chan=1):
        """Measure channel power

        Args:
            chan (int): channel number

        Returns:
            power (float): channel power
        """
        return float(self.query(f':MEAS:POWE? CH{chan}'))
