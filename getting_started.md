Setup + Interacting
===================

This section explains how to get koebi up and running with the default firmware and tablet GUI. This combination allows to control the **speed** and **position** of the six stepper motors **independently** or **pairwise coordinated moves**.

Firmware
--------

Use the [esptool](https://github.com/espressif/esptool) to flash this Micropython build on the ESP32. It is easily installed using pip:

```
$ pip install esptool
```

If you put Micropython on your board for the first time, it should be erased first:

```
$ esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
```

After this, the custom firmware can be flashed:

```
$ cd (...)/koebi/firmware
$ esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 406800 write_flash -z --flash_mode dio --flash_freq 40m 0x1000 firmware.bin
``` 

For more information, see the [official Micropython docs](https://micropython.org/download#esp32).


Setup the TouchOSC GUI
----------------------

- Install the [TouchOSC](https://hexler.net/products/touchosc) app on a tablet.  
It's a paid app (5.-, sorry about that)

- Install the application to edit layouts, [TouchOSC Editor](https://hexler.net/products/touchosc#downloads), on a computer (free)

- Transfer the ``koebi.touchosc`` (found in ``/gui``) to the tablet. The official documentation walks you through this for [iOS](https://hexler.net/docs/touchosc-configuration-layout-transfer-wifi?ios) and [Android](https://hexler.net/docs/touchosc-configuration-layout-transfer-wifi?android)

To complete the setup, you need to specify a few options on the tablet. Access these by tapping the **dot** at the **top right corner** in the TouchOSC app.

Set the following **Host**:

- Host: ``192.168.4.1`` (which is the ESP32's IP Address)
- Port (outgoing): ``8000``
- Port (incoming): ``9000``

And under **Options**:

- Send Ping (``/ping``): ``On``
- Delay: ``5s`` 

Finally, make sure to connect with the systems WiFi:
- Network name (SSID): ``koebi``
- No password / encryption

When opening TouchOSC, you should now be able to power up the motors and control them. 

Open Sound Control (OSC) API
============================

The tablet uses the following API to communicate with the ESP32. It is implemented in ``main.py`` and can be used by any other client within ``koebis``'s network to control it.  
 
**Feedback Behaviour**:

**Need more?** Read the [hacking guide](hacking.md).

Globals
-------

### ``/fan``
Enable or disable the fan cooling the stepper drivers (0/1)

### ``/power``
Enable or disable the stepper drivers output. Starts the fan upon enabling, and stops it upon disabling (0/1).  
**Heads up**: Always disable the stepper outputs before pulling koebi's cord. Otherwise, the Trinamic stepper drivers may **be permanently damaged due to overvoltage spikes**!

### ``/reset``
Trigger a software reset of the ESP32 board (0/1)

Stepper Motor Globals
---------------------

### ``/all/curr``
Set all steppers' run current, specified in milliamperes (100..1200). High values (>800) may lead to thermal shutdown in a heavy-use scenario.
### ``/all/acc``
Set all steppers' acceleration, in cm/s<sup>2</sup> (0.1…200)
### ``/all/vel_limit``
Set all stepper's max velocity, in cm/s (0…200)


## Individual Stepper Motor Commands
For each of the following endpoints, ``[motor]`` may be ``a``, ``b``, ``c``, ``d``, ``e`` or ``f``.

### ``/[motor]/vel``
Set a steppers velocity as a factor of the velocity limit (0 … 1).  
### ``/[motor]/zero``
Define a steppers current position as the new ``0.0``, ie. home position (0/1)
### ``/[motor]/end``
Define a steppers current position as the new ``1.0``, ie. end position (0/1)
### ``/[motor]/target``
Set a steppers target position as a factor of the motor's axis length (0…1)
### ``/[motor]/pos``
Get a steppers current position as a factor of the motor's axis length (0…1)