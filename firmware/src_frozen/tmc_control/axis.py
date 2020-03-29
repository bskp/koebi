
import utime, math
from machine import PWM, Timer
from esp32 import MCPWM
from remote import rate_limit



class LFO:
    ''' Low-frequency Oscillator '''
    tau = math.pi*2

    def __init__(self):
        self.phase = 0  # e 0..1, not 0..tau
        self.freq = 1.0
        self.amp = 0
        self.center = 0.5 # phase center, e 0..1
        self.val = 0
        self._ms = 0  # for #tick


    def biased_phase(self):
        if self.phase < self.center:
            return 0.5*self.phase/self.center
        
        return 1 - 0.5*(1 - self.phase)/(1 - self.center)


    def tick(self):
        ms = utime.ticks_ms()
        dt = (ms - self._ms)/1000
        self._ms = ms
        self.phase += dt*self.freq

        # Truncate to allow for long-term precision
        if self.phase > 1:
            self.phase = self.phase % 1

        self.val = self.amp*math.cos(self.biased_phase()*LFO.tau)


class Axis:
    ''' A stepper motor driven axis. '''

    instances = []
    timer = Timer(-1)
    timer_is_init = False
    pilot_hz = 50

    lfos = [LFO() for i in range(3)]

    class State:
        STOP = 0
        ACC = 1
        DECC = 2
        TRAVEL = 3
        MANUAL = 4

    @rate_limit(1000)
    def update_load(self):
        if self.track_load:
            self.load = self.chopper.mech_load()
            print(self.load)
        else:
            self.load = 0

    @classmethod
    def driver_callback(cls, timer):
        ''' Use only one timer for all axis instances. '''

        for lfo in cls.lfos:
            lfo.tick()

        for instance in cls.instances:
            instance._pilot()


    def __init__(self, chopper, dir_pin, pwm):
        if type(pwm) is not PWM and type(pwm) is not MCPWM:
            raise TypeError("Either a machine.PWM or esp32.MCPWM instance is expected")

        self.chopper = chopper
        self.dir_pin = dir_pin
        self.pwm = pwm

        # Default configs
        self.state = Axis.State.STOP
        self.units_per_rev = 12.6  # pi*4cm, units being cm.
        self.target = 0  # units
        self.position = 0   # units
        self.eff_position = 0   # units
        self.speed = 0      # units/s
        self.acc = 30       # units/s^2
        self.top_speed = 80 # units/s
        self.length = 200   # units

        self.steps_per_rev = 200

        # Fields for sync'd piloting
        self.restore_acc = None
        self.restore_top_speed = None

        self.lfos = set()

        # Init peripherals
        chopper.sane()
        self.microstepping(4)
        chopper.set_current(500)

        self.track_load = False
        self.load = 0

        self.pwm.duty(0)
        self.dir_pin.on()
        self.dir = 1

        self.set_speed = Axis.DistanceTracker(self)

        # Init class-owned timer
        Axis.instances.append(self)
        if not Axis.timer_is_init:
            ms = int(1000/Axis.pilot_hz)
            Axis.timer.init(period=ms, mode=Timer.PERIODIC, callback=Axis.driver_callback)
            Axis.timer_is_init = True


    def __del__(self):
        # Not yet supported by Micropython.
        Axis.instances.remove(self)


    def _pilot(self):
        # This method is invoked periodically by the class' timer

        acc = self.dir*self.acc/Axis.pilot_hz  # speed change for this control step

        speed_ = self.speed

        if self.state is Axis.State.ACC:
            speed_ = self.speed + acc
            if abs(speed_) > abs(self.top_speed):
                speed_ = self.top_speed*self.dir
                self.state = Axis.State.TRAVEL

        if self.state is Axis.State.DECC:
            speed_ = self.speed - acc

            # Do we have to stop?
            if self.dir*(speed_) < 0:
                speed_ = 0
                self.state = Axis.State.STOP

                # Check if target was missed (typically if a new target was issued)
                if abs(self.position - self.target) > 2.0:
                    self.set_target(self.target)

        # Invoking set_speed also updates this axis' position. Therefore, it is always called. #sorryforugly.
        self.set_speed(speed_)

        if self.state is not Axis.State.TRAVEL and self.state is not Axis.State.ACC:
            return

        # Decide whether to start braking now.

        pos_after_braking = self.position + self.braking_distance()

        tol = abs(self.speed/Axis.pilot_hz*1.5)
        if self.dir*(self.target - pos_after_braking) < tol:
            self.state = Axis.State.DECC


    def braking_distance(self):
        return self.dir*self.speed*self.speed/self.acc/2


    def set_zero(self):
        self.position = 0
        self.eff_position = 0
        self.target = self.position 


    def set_length(self):
        self.length = self.position
        self.target = self.position


    def set_target(self, target):
        if target < 0:
            print("Target moved to 0")
            target = 0

        if target > self.length:
            print("Target moved to end (%.1f)" % self.length)
            target = self.length

        distance = target - self.position
        self.target = target
        self.dir = 1 if distance > 0 else -1
        self.dir_pin.value(True if distance > 0 else False)
        self.state = Axis.State.ACC

        # reset possible "dirty state" from previous/ongoing synched movement
        if self.restore_acc:
            self.acc = self.restore_acc
        if self.restore_top_speed:
            self.top_speed = self.restore_top_speed



    def microstepping(self, divider_exponent=4, interpolate=True):
        '''
        Set the microstepping factor to 256/2^<divider_exponent>. The optional arguments"interpolate" can be set false to
        disable driver-internal interpolation to 256 microsteps.
        '''
        self.microsteps = int(256/2**divider_exponent)
        self.chopper.chopconf().intpol(interpolate).mres(divider_exponent).dedge(0).push()


    class DistanceTracker:
        def __init__(self, axis):
            self.axis = axis
            self.last_change = utime.ticks_us()
            self.eff_dir = 1
            self.eff_speed = 0

        def __call__(self, units_per_s):
            a = self.axis

            # Set "high-level" direction and speed (without LFOs)
            a.dir = 1 if units_per_s > 0 else -1

            # Enforce speed limit
            if abs(units_per_s) > abs(a.top_speed):
                units_per_s = a.dir*a.top_speed

            a.speed = units_per_s

            # Mix in LFOs
            self.eff_speed = units_per_s
            for lfo in a.lfos:
                self.eff_speed += lfo.val

            # Truncate precision
            hz = int(self.eff_speed/a.units_per_rev*a.steps_per_rev*a.microsteps)

            # Update axis direction
            if hz < 0:
                a.dir_pin.off()
                self.eff_dir = -1

            elif hz > 0:
                a.dir_pin.on()
                self.eff_dir = 1

            if hz == 0:
                a.pwm.duty(0)
            else:
                a.pwm.duty(50)
                a.pwm.freq(abs(hz))

            # Position bookkeeping
            ts = utime.ticks_us()
            eff_travelled = (ts - self.last_change)*self.eff_speed/1000000
            travelled = (ts - self.last_change)*a.speed/1000000
            a.position += travelled
            a.eff_position += eff_travelled

            self.last_change = ts
