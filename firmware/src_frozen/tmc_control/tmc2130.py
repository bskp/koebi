# pylint: disable=no-member

import utime
from machine import Pin, SPI
from ustruct import pack, unpack
from machine import PWM


class Tmc2130:
    ''' A Trinamic TMC2130 stepper motor driver connected via SPI. '''


    def __init__(self, spi, chip_select):
        '''
        Connect to a TMC2130 via SPI. The passed SPI has to use SPI_MODE=3 (ie. pol=1, phs=1) and MSB-first transmission.

        ``chip_select`` can be either a hardware Pin, or a tuple of two callbacks for activating / deactivating the
        corresponding chip select line.
        The CS input on the TMC2130 is active-low. Example:

        spi = SPI(2, baudrate=1000000, polarity=1, phase=1, firstbit=SPI.MSB, sck=Pin(18), miso=Pin(19), mosi=Pin(23))
        cs_a = Pin(5, Pin.OUT)
        motor_a = Tmc2130(spi, chip_select=(cs_a.off, cs_a.on))
        TODO update

        '''

        self.spi = spi
        self._current = None

        # Chip select handlers
        if isinstance(chip_select, tuple):
            self.cs_enable = chip_select[0]
            self.cs_disable = chip_select[1]
        else:
            self.cs_enable = chip_select.off
            self.cs_disable = chip_select.on

        # Register definitions

        self.status = Register(self, None, 'Status flags from previous read access', Access.R, {
            'stst': (3, 'Standstill indicator'),
            'stallGuard': (2, 'Motor stall detected'),
            'drv_err': (1, 'Overtemperature or short circuit shutdown'),
            'reset': (0, 'IC reset occurred since last read of GSTAT')
        })
        self.__statusbyte = 0x00

        self.gconf = Register(self, 0x00, 'Global configuration flags', Access.RW, {
            'i_scale_analog': (0, 'Current scaling by analog reference'),
            'internal_Rsense': (1, 'Internal current sense resistors'),
            'en_pwm_mode': (2, 'Enable stealthChop PWM mode'),
            'shaft': (4, 'Invert shaft direction'),
            'diag0_error': (5, 'Enable DIAG0 on driver errors'),
            'stop_enable': (15, 'Emergency stop'),
        })

        self.gstat = Register(self, 0x01, 'Global status', Access.RC, {
            'reset': (0, 'IC reset occurred since last read of GSTAT'),
            'drv_err': (1, 'Indicates that the driver has been shut down due to overtemperature or short circuit detection' +
                        'since the last read access. Read DRV_STATUS for details.'),
            'cp_uv': (2, 'The internal charge pump encountered an undervoltage. In such a case, the driver is disabled')
        })

        self.ioin = Register(self, 0x04, 'Physical input pins', Access.R, {
            'step':     (0, 'STP'),
            'dir':      (1, 'DIR'),
            'dcen_cfg4':(2, 'DC_EN / CFG4'),
            'dcin_cfg5':(3, 'DCIN / CFG5'),
            'dco':      (4, 'DCO'),
            'version':  ((24, 31), 'IC version, always 17 == 0x11')
        })

        self.ihold_run = Register(self, 0x10, 'Driver current control', Access.W, {
            'ihold':        ((0, 4), 'Standstill current in units of 1/32'),
            'irun':         ((8, 12), 'Motor run current in units of 1/32'),
            'iholddelay':   ((16, 19), 'Time for motor power down transition after standstill detection ' +
                             'and TWPOWERDOWN expiration in multiples of 2^18 clock cycles.')
        })

        self.tpowerdown = Register(self, 0x11, '', Access.W, {
            'tpowerdown': ((0, 8), 'Delay for motor power down after standstill detection in multiples of 2^18 clock cycles')
        })

        self.tstep = Register(self, 0x12, 'Measured time between two 1/256 microsteps', Access.R, {
            'tstep': ((0, 20), 'Measured time between two 1/256 microsteps in units of 1/fCLK')
        })

        self.tpwmthrs = Register(self, 0x13, 'Upper velocity for stealthChop voltage PWM mode', Access.W, {
            'tpwmthrs': ((0, 20), 'tstep >= tpwmthrs => dcStep off, stealthChop PWM on'),
        })

        self.tcoolthrs = Register(self, 0x14, 'Lower velocity for coolStep and stallGuard', Access.W, {
            'tcoolthrs': ((0, 20), 'Set this par. to disable coolStep at low speeds, where it cannot work reliably')
        })

        self.thigh = Register(self, 0x15, 'Lower velocity for higher-torque stepper mode', Access.W, {
            'thigh':    ((0, 20), 'Disables coolStep, stealthChop, sets vhigh options')
        })

        self.chopconf = Register(self, 0x6C, 'Chopper and driver configuration', Access.RW, {
            'diss2g':   (30, 'Short to GND protection is: 0 = on, 1 = off'),
            'dedge':    (29, 'Enable double edge step pulses'),
            'intpol':   (28, 'Interpolation to 256 microsteps enabled'),
            'mres':     ((24, 27), 'Microstep divider. Nr of microsteps = 256/2^mres'),
            'sync':     ((20, 23), 'Pwm sync clock. Switched off above VHIGH.'),
            'vhighchm': (19, 'Switch to chm=1 and fd=0 for velocities above VHIGH.'),
            'vhighfs':  (18, 'Switch to fullstep for velocities above VHIGH.'),
            'vsense':   (17, 'Sense voltage scaling. 0 = low, 1 = high sensitivity'),
            'tbl':      ((15, 16), 'Comparator blank time. 00 = 16, 01 = 24, 10 = 36, 11 = 54 clocks'),
            'chm':      (14, 'Chopper mode. 0 = Standard (SpreadCycle), 1 = constant off time'),
            'rndtf':    (13, 'Random TOFF time. 0 = off, 1 = modulate TOFF'),
            'disfdcc':  (12, 'Fast decay mode, for chm == 1.'),
            'fd3':      (11, 'MSB of fast decay time setting TFD. Num of fast decay clock cycles = 32*TFD'),
            'hend':     ((7, 10), 'Set hysteresis low value (chm == 0) or offset (chm == 1) to -3 (0), … 12 (16)'),
            'hstrt':    ((4, 6), 'chm == 0: Add 1 … 8 to HEND; chm == 1: bits 0-2 for fast decay setting TFD. s. fd3.'),
            'toff':     ((0, 3), 'Off time (slow decay phase). 0 = Driver disable, 1 = Use only with TBL >= 2. N_clk = 12 * 32*TOFF.')
        })

        self.coolconf = Register(self, 0x6C, 'coolStep and stallGuard2 configuration', Access.W, {
            'sfilt':    (24, 'Enable LP-filter for stallGuard2 signal'),
            'sgt':      ((16, 22), 'Stall detection threshold value (signed), -64 … 63'),
            'seimin':   (15, 'Minimum current for smart current control. 0 = 1/2, 1 = 1/4 * IRUN'),
            'sedn':     ((13, 14), 'Current decrease factor'),
            'semax':    ((8, 11), 'stallGuard2 hysteresis value for smart current control'),
            'seup':     ((5, 6), 'Current increment steps per SG2-value'),
            'semin':    ((0, 3), 'Minimum sG2-value for smart current control')
        })

        # dcctrl

        self.drv_status = Register(self, 0x6F, 'Stallguard and driver error flags', Access.R, {
            'stst': (31, 'Standstill indicator'),
            'olb': (30, 'B: Open load'),
            'oba': (29, 'A: Open load'),
            's2gb': (28, 'B: Short to ground'),
            's2ga': (27, 'A: Short to ground'),
            'otpw': (26, 'Overtemperature warning'),
            'ot': (25, 'Overtemperature detected'),
            'stallGuard': (24, 'Motor stall detected'),
            'cs_actual': ((16, 20), 'Actual current scaling'),
            'fsactive': (15, 'Full step active'),
            'sg_result': ((0, 9), 'Mechanical load measurement')
        })

        self.pwmconf = Register(self, 0x70, 'PWM configuration', Access.W, {
            'freewheel': ((20, 21), 'Stand still options when motor current is zero. 0 = normal, 1 = freewheeling, 2 = coil to LS, 3 = coil to HS'),
            'pwm_symmetric': (19, 'Force symmetric PWM'),
            'pwm_autoscale': (18, 'PWM automatic amplitude scaling'),
            'pwm_freq': ((16, 17), 'PWM frequency selection. 0 = 2/1024, 1 = 2/683, 2 = 2/512, 3 = 2/410 * f_clk'),
            'pwm_grad': ((8, 15), 'User defined amplitude (gradient) or regulation loop gradient'),
            'pwm_ampl': ((0, 7), 'User defined amplitude (offset)')
        })

        # pwm_scale
        # encm_ctrl

        self.lost_steps = Register(self, 0x73, 'Lost steps due to overload', Access.R, {
            'lost_steps': ((0, 20), 'Counts up or down depending on direction. Only with SDMODE=1')
        })

        self.check_spi()


    def check_spi(self):
        if self.ioin().version() != 0x11:
            print('TMC does not return a correct HW version. Is it connected properly?')


    def sane(self):
        ''' Initialization example from p. 84 in the TMC2130 datasheet. One deviation: the choppers are not activated (TOFF).'''

        (self.chopconf()
         .toff(0) # slow decay phase = 12 * 32*3 clock cycles
         .hend(3) # Set hysteresis to -2
         .hstrt(4) # add 5 to the hysteresis low value HEND
         .tbl(2) # Set comparator blank time to 24 clock cycles
         .chm(0) # Standard chopper mode (spreadCycle)
         .push()
        )

        (self.ihold_run()
         .ihold(10) # Set standstill current to 11/32
         .irun(31) # Set motor run current to 32/32
         .iholddelay(6) # Set timeout for motor power down after standstill and
         # TPOWERDOWN expiration to 6*2^18 clock cycles
         .push()
        )

        self.tpowerdown().tpowerdown(10).push()
        # Set motor current power down timeout after standstill to 10*2^18 clock cycles

        self.gconf().en_pwm_mode(1).push()

        self.tpwmthrs().tpwmthrs(500).push()  # 35 kHz -> 30 RPM
        # Upper velocity for stealthChop voltage PWM mode.

        (self.pwmconf()
         .pwm_autoscale(1)
         .pwm_freq(0)
         .pwm_ampl(200)
         .pwm_grad(1)
         .push()
        )

        self.set_current(300)


    def set_current(self, mA, hold_factor=0.5, Rsense=0.11):
        cc = self.chopconf()
        self._current = mA

        current_scale = 32*1.41421*mA/1000*(Rsense+0.02)/0.325 - 1
        cc.vsense(0)

        if current_scale < 16:
            current_scale = 32*1.41421*mA/1000*(Rsense+0.02)/0.180 - 1
            cc.vsense(1)

        cc.push()

        (self.ihold_run()
         .irun(current_scale)
         .ihold(current_scale*hold_factor)
         .push()
        )

    def get_current(self):
        return self._current


    def mech_load(self):
        return 1 - self.drv_status().sg_result()/128  # 128 is arbitrary.


    def stallguard(self, set=None):
        if not set:
            return self.coolconf().sgt()

        self.coolconf().sgt(set).push()


    def stealthchop(self, set=None, threshold=None):
        if set is None:
            return self.gconf().en_pwm_mode()
        
        self.gconf().en_pwm_mode(set).push()

        if threshold:
            self.tpwmthrs().tpwmthrs(threshold).push()


    def off(self):
        ''' Disable the power outputs for eg. save shutdown. '''
        self.chopconf().toff(0).push()


    def on(self):
        ''' Enable the power outputs. '''
        self.chopconf().toff(3).push()


    def __write(self, register, data):
        #print("\tWrite to (%02X):  %08X" % (register, data))

        datagram = bytearray(5)
        datagram[0] = 0b10000000 | register
        datagram[1:] = pack("!I", data)  # pack as big-endian uint32

        self.cs_enable()
        utime.sleep_ms(5)
        self.spi.write(datagram)
        self.cs_disable()


    def __read(self, register):
        datagram = bytearray(5)
        datagram[0] = 0b01111111 & register
        utime.sleep_ms(5)

        # Send register to read
        self.cs_enable()
        utime.sleep_ms(5)
        self.spi.write(datagram)
        self.cs_disable()

        # Fetch requested data
        self.cs_enable()
        utime.sleep_ms(5)
        datagram = self.spi.read(5)
        self.cs_disable()

        self.__statusbyte = datagram[0]
        return int.from_bytes(datagram[1:], 'big')


    def get_status(self):
        print(ShadowRegister(self.status, self.__statusbyte))



class Register:
    def __init__(self, ic, address, label, mode, fields):
        self.address = address
        self.mode = mode
        self.label = label
        self.ic = ic
        self.offsets = {field: bits_and_desc[0] for (field, bits_and_desc) in fields.items()}
        self.descriptions = {field: bits_and_desc[1] for (field, bits_and_desc) in fields.items()}


    def __call__(self, rr=None):
        # Get
        if rr is None:
            if self.address is None:
                return ShadowRegister(self, self.ic.__statusbyte)

            data = self.ic.__read(self.address)
            return ShadowRegister(self, data)

        # Set
        if not isinstance(rr, ShadowRegister):
            raise TypeError("A modified RegisterReadout is expected")

        if not rr.reg is self:
            raise ValueError("Register mismatch")

        self.ic.__write(self.address, rr.data)



class ShadowRegister:
    def __init__(self, reg, data):
        self.reg = reg
        self.data = data

        # Create getter/setter methods for each field in this register
        for id in self.reg.offsets:
            setattr(self, id, self.__handler_closure(id))


    def push(self):
        ''' Write the register data to its source IC. '''
        self.reg.ic.__write(self.reg.address, self.data)


    def bin(self):
        print("0b{0:032b}".format(self.data))


    def hex(self):
        print("0x{0:08X}".format(self.data))


    def __handler_closure(self, id):
        def handler(overwrite=None):
            ''' Invoke without arguments to get this field, or modify it by passsing a value.'''
            bits = self.reg.offsets[id]
            if not isinstance(bits, tuple):
                bits = (bits, bits)

            bitmask = ( 0xFFFFFFFF >> (31 - bits[1] + bits[0]) ) << bits[0]

            # Read access
            if overwrite is None:
                return (self.data & bitmask) >> bits[0]

            # Write access
            databits = int(overwrite) << bits[0]
            self.data = (self.data & ~bitmask) | (databits & bitmask)
            return self

        return handler


    def __str__(self):
        addr = self.reg.address if self.reg.address else 0xFF
        out = '<Register 0x%02x: %s>' % (addr, self.reg.label)
        for id, desc in self.reg.descriptions.items():
            getter = getattr(self, id)
            val = getter()
            out += "\n%15s: %3s    %s" % (id, val, desc)
        return out


    def __repr__(self):
        return self.__str__()


class Access:
    R = 1
    W = 2
    RW = 3
    RC = 0
