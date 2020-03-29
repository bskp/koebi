# Extend the Micropython Firmware

If you want to "freeze" a python module to free up RAM, or if you want to extend any of the frozen/native modules ``TMC`` or ``MCPWM``, you'll need to re-compile the firmware.

The process is fully described in the [esp32 port's README.md](https://github.com/micropython/micropython/blob/master/ports/esp32/README.md), but is mostly already taken care of. Start by initializing this repo's submodules:

~~~ bash
$ git submodule update --init --recursive
~~~

This clones the nested repos at ``/firmware/frameworks/``, which are the following projects:

### Micropython
The [referenced micropython fork](https://github.com/bskp/micropython_esp32_mcpwm/tree/micropython-for-koebi) supports the ESP32's **MCPWM**-Module, standing for _Motor control Pulse-Width-Modulation_. This was required to have enough PWM outputs available (6 modules).  
Read more about the MCPWM in [Espressif's API documentation](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/mcpwm.html)!

### ESP-IDF
For better MCPWM-frequency update behaviour, we use a [minimally modified](https://github.com/espressif/esp-idf/compare/release/v3.3...bskp:dev-mcpwm-synched-updates) variant of the esp-idf, v3.3.1.

The _Micropython ESP32 port_'s Makefile located at ``firmware/frameworks/micropython/ports/esp32`` should already have the correct commit referenced, which was checked out while initializing the submodules:

~~~ Makefile
...
# The git hash of the currently supported ESP IDF version.
# These correspond to v3.3.1 and v4.0.
ESPIDF_SUPHASH_V3 := cc02b01ea59e112e6ccf7fc3b66f3624f5d41167  # patched MCPWM update behaviour, based upon v3.3.1
ESPIDF_SUPHASH_V4 := 463a9d8b7f9af8205222b80707f9bdbba7c530e1
...
~~~

### Frozen Modules

The last puzzle piece is the stepper-driver specific python package ``tmc_control``, located at ``firmware/src_frozen``.

Since it contains mappings for _almost all_ of TMC2130's registers, this uses up a ton of RAM if loaded dynamically. Therefore, they are better ["frozen" into the Micropython](http://docs.micropython.org/en/latest/reference/constrained.html) firmware.

This is achieved by copying the modules from ``/firmware/src_frozen`` to ``/firmware/frameworks/micropython/ports/esp32/modules``:

- tmc_control
    - __init__.py
    - axis.py
    - tmc2130.py
- uasyncio
    - __init__.py
    - core.py
- uftpd.py

(Actually, the latter two, ``uasyncio`` and ``uftpd`` should already be there.)


### Configuration

The remaining steps are explained in more detail in ``ports/esp32/README.me``. 

The environment variables for the build process are defined in ``GNUMakefile``, which takes precedence over ``Makefile``:

~~~ Makefile
ESPIDF = ../../../esp-idf
BOARD = GENERIC
PORT = /dev/tty.usbserial-DN05LWXG
FLASH_MODE = dio
FLASH_SIZE = 4MB
CROSS_COMPILE = $(ESPIDF)/xtensa-esp32-elf/bin/xtensa-esp32-elf-

include Makefile
~~~~

Make sure to adjust the ``PORT`` according to your setup!

### Compiling

See the [esp32 port's README.md](https://github.com/micropython/micropython/blob/master/ports/esp32/README.md) for troubleshooting.

~~~ bash
$ cd mpy-cross
$ make mpy-cross

$ cd ../ports/esp32
$ make clean
$ make submodules
$ make deploy # erases the ESP32's firmware and uploads!
~~~
