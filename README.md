# Rigol Control for DM3058 and DP821

# Install

    sudo echo 'SUBSYSTEMS=="usb", ATTRS{idVendor}=="1ab1", GROUP="dialout", MODE="0666"' > /etc/udev/rules.d/30-rigol.rules

    pip install https://github.com/evidlo/rigol_stuff/archive/master.zip
    
# Examples

``` python
from rigol_stuff.rigol import RigolDM305, RigolDP821
>>> r = RigolDM3058(vendor="0x1ab1", product="0x09c4", serial="DM3L223900431")
>>> r.meas_current()
```

``` python
# power supply
>>> dcps = RigolDP821(vendor="0x1ab1", product="0x0e11", serial="DP8G194400109")
>>> dcps.reset()
>>> dcps.set_voltage(voltage=v, max_current=0.5)
>>> dcps.turn_on()
>>> time.sleep(1)
>>> dm.meas_voltage()
0.0001432987
>>> dcps.turn_off()
>>> dcps.close()

# multimeter
>>> dm = RigolDM3058(vendor="0x1ab1", product="0x09c4", serial="DM3L223900431", debug=True)
>>> dm.reset()
>>> dm.meas_voltage()
0.0001432987
>>> dm.meas_current()
-0.0001834927
>>> dm.close()
```
