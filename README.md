# Rigol Control for DM3058 and DP821

# Install

    sudo echo 'SUBSYSTEMS=="usb", ATTRS{idVendor}=="1ab1", GROUP="dialout", MODE="0666"' > /etc/udev/rules.d/30-rigol.rules
    pip install https://github.com/evidlo/rigol_stuff/archive/master.zip
    
# Examples

Get the vendor/product/serial numbers from the output of `lsusb -v`

    $ lsusb -v | grep Rigol -A 50 | grep 'iProduct\|idProduct\|idVendor\|iSerial'
    idVendor           0x1ab1 Rigol Technologies
    idProduct          0x09c4 
    iProduct                2 DM3000 SERIES 
    iSerial                 3 DM3L22XXXXXXX



``` python
from rigol_stuff.rigol import RigolDM305, RigolDP821
# multimeter
>>> dm = RigolDM3058("DM3L22XXXXXXX")
>>> dm.reset()
>>> dm.meas_voltage()
0.0001432987
>>> dm.meas_current()
-0.0001834927
>>> dm.close()

# power supply
>>> dcps = RigolDP821("DP8G19XXXXXXX")
>>> dcps.reset()
>>> dcps.set_voltage(voltage=v, max_current=0.5)
>>> dcps.turn_on()
>>> time.sleep(1)
>>> dm.meas_voltage()
0.0001432987
>>> dcps.turn_off()
>>> dcps.close()
```
