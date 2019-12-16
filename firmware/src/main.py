import micropython, gc
from machine import SPI, Pin, Timer, reset
from esp32 import MCPWM

import time

from uosc.client import Client, Bundle, create_message
from tmc_control import Tmc2130, Axis, AllAxes, LFO

from async_server import serve, run_server
from uasyncio import get_event_loop

from remote import Page, Control, ControlTuple, Tracker, rate_limit, Label

last_alloc = 0
def mem(label=''):
    global last_alloc
    gc.collect()
    diff = gc.mem_alloc() - last_alloc
    last_alloc = gc.mem_alloc()
    print("%20s: %4.1f    / %4.1f free" % (label, diff/1024, gc.mem_free()/1024) )

mem("imports")

fan_pin = Pin(13, Pin.OUT)
fan_pin.on()

# Check if pins 12 and 13 are connected (stepper board detection)
aux0_pin = Pin(12, Pin.IN)
on_board = True

if aux0_pin.value() != 1:
    on_board = False

fan_pin.off()
if aux0_pin.value() != 0:
    on_board = False

# Define SPI chip select pins.

cs0 = Pin(2, Pin.OUT)
cs1 = Pin(15, Pin.OUT)
cs2 = Pin(5, Pin.OUT)

def cs(idx=0):
    cs0.value(idx & 0b001)
    cs1.value(idx & 0b010)
    cs2.value(idx & 0b100)

spi = SPI(2, baudrate=1000000, polarity=1, phase=1, firstbit=SPI.MSB, sck=Pin(18), miso=Pin(19), mosi=Pin(23))

mem("spi")

dir_a = Pin(16, Pin.OUT)
pwm_a = MCPWM(0)
pwm_a.bind(Pin(17))

mem("a")

dir_b = Pin(4, Pin.OUT)
pwm_b = MCPWM(1)
pwm_b.bind(Pin(0))

mem("b")

# Activating Output C collides with UART-over-USB (same pins).
# Therefore, it is only activated when the the Jumper between pins 12 and 13 is present.
dir_c = Pin(3 if on_board else 22, Pin.OUT)
pwm_c = MCPWM(2)
pwm_c.bind(Pin(1 if on_board else 25))

dir_d = Pin(32, Pin.OUT)
pwm_d = MCPWM(3)
pwm_d.bind(Pin(33))

dir_e = Pin(25, Pin.OUT)
pwm_e = MCPWM(4)
pwm_e.bind(Pin(26))

dir_f = Pin(27, Pin.OUT)
pwm_f = MCPWM(5)
pwm_f.bind(Pin(14))

mem("d, e, f")

mem("chopper a")
chopper_a = Tmc2130(spi, (lambda: cs(5), cs))
chopper_b = Tmc2130(spi, (lambda: cs(6), cs))
chopper_c = Tmc2130(spi, (lambda: cs(4), cs))
chopper_d = Tmc2130(spi, (lambda: cs(1), cs))
chopper_e = Tmc2130(spi, (lambda: cs(2), cs))
chopper_f = Tmc2130(spi, (lambda: cs(3), cs))

mem("choppers")

a = Axis(chopper_a, dir_a, pwm_a)
b = Axis(chopper_b, dir_b, pwm_b)
c = Axis(chopper_c, dir_c, pwm_c)
d = Axis(chopper_d, dir_d, pwm_d)
e = Axis(chopper_e, dir_e, pwm_e)
f = Axis(chopper_f, dir_f, pwm_f)

mem("axes")

axes = {
    'a': a,
    'b': b,
    'c': c,
    'd': d,
    'e': e,
    'f': f
}

osc_client = None

mem("osc client")

def sing(axis, note, duration=200):
    base = 1 # cm/s
    vel = base*math.pow(2, note/12)

    axis.set_speed(vel)
    time.sleep_ms(int(duration))

    axis.set_speed(0)


class Vel(Page):

    def update_acc(self, val):
        for axis in axes.values():
            axis.acc = val
            axis.restore_acc = val

    def update_curr(self, val):
        for axis in axes.values():
            axis.chopper.set_current(val)

    def update_vel(self, val):
        for axis in axes.values():
            axis.top_speed = val
            axis.restore_top_speed = None

    def update_power(self, val):
        if val:
            [a.chopper.on() for a in axes.values()]
            self.fan.set(1)
        else:
            [a.chopper.off() for a in axes.values()]
            self.fan.set(0)

        if not on_board:
            chopper_c.off()
        print("Motors %s" % ("on" if val else "off") )


    def update_stallguard(self, val):
        for axis in axes.values():
            axis.track_load = val


    def init_controls(self):
        self.acc = Control('/all/acc', (0.1, 200), Control.QUADRATIC, action=self.update_acc, feedback=True)
        self.acc.set(80)
        self.current = Control('/all/current', (100, 1200), action=self.update_curr, feedback=True)
        self.current.set(300)
        self.vel_limit = Control('/all/vel_limit', (0, 200), Control.QUADRATIC, action=self.update_vel, feedback=True)
        self.vel_limit.set(80)

        self.reset = Control('/reset', action=lambda _: reset())
        self.fan = Control('/fan', action=fan_pin.value, feedback=True)
        self.power = Control('/power', action=self.update_power, feedback=True)

        for label, axis in axes.items():
            vel_src = Tracker(axis, 'speed')
            vel = Control('/' + label + '/vel', (None, self.vel_limit), Control.QUADRATIC, action=axis.set_speed, source=vel_src)

            def reset_for(v):
                return lambda _: v.set(0)

            stop = Control('/' + label + '/stop', (0, 1), action=reset_for(vel))
            # load = Control('/' + label + '/load', (0, 1), Tracker(axis, 'load'))

            setattr(self, 'vel_' + label, vel)
            setattr(self, 'stop_' + label, stop)
            # setattr(self, 'load_' + label, load)

        def make_noise(on):
            for axis in axes.values():
                if on:
                    axis.microstepping(6, False)
                    axis.chopper.stealthchop(False)
                else:
                    axis.microstepping(4, True)
                    axis.chopper.stealthchop(True)

        self.make_noise = Control('/all/stealthchop', action=make_noise, feedback=True)
        self.make_noise.set(0)
        self.stallguard = Control('/all/stallguard', action=self.update_stallguard, feedback=True)
        self.stallguard.set(0)

vel = Vel('velocity')



class Pos(Page):

    def init_controls(self):
        self.starts = {}
        self.ends = {}
        self.targets = {}
        self.poss = {}
        self.homes = {}

        for label, axis in axes.items():
            length = Tracker(axis, 'length')
            pos_rd = Tracker(axis, 'eff_position')
            target_tr = Tracker(axis, 'target')

            def start_for(v):
                return lambda _: v.set_zero()

            def end_for(v):
                return lambda _: v.set_length()

            def home_for(v):
                return lambda _: v.set_target(0)

            start = Control('/' + label + '/zero', action=start_for(axis))
            end = Control('/' + label + '/end', action=end_for(axis))
            target = Control('/' + label + '/target', (0, length), source=target_tr, action=axis.set_target)
            pos = Control('/' + label + '/pos', (0, length), source=pos_rd)
            home = Control('/' + label + '/home', action=home_for(axis))

            self.starts[axis] = start
            self.ends[axis] = end
            self.targets[axis] = target
            self.poss[axis] = pos
            self.homes[axis] = home

pos = Pos('position')



class XY(Page):

    def set_2d_target(self, l, r):
        if self.x:
            self.x.set_target(l)
        if self.y:
            self.y.set_target(r)

        if self.x and self.y and self.sync():
            dx = abs(self.x.target - self.x.position)
            dy = abs(self.y.target - self.y.position)

            fast = self.x if dx > dy else self.y
            slow = self.y if dx > dy else self.x

            factor = dy/dx if dx > dy else dx/dy
            print("factor for %s: %.2f" % (slow, factor))

            slow.acc = fast.acc*factor
            slow.top_speed = fast.top_speed*factor

            slow.restore_acc = fast.acc
            slow.restore_top_speed = fast.top_speed

        return


    def init_controls(self):
        self.x = None
        self.y = None

        self.sync = Control('/2dpad/sync', feedback=True)
        self.sync.set(True)

        self.pos = ControlTuple('/2dpad/pos')
        self.target = ControlTuple('/2dpad/target', action=self.set_2d_target)

        self.acc = vel.acc
        self.vel_limit = vel.vel_limit
        self.current = vel.current

        def set_x_for(axis):
            def setter(active):
                pos_control = pos.poss[axis] if active else None
                target_control = pos.targets[axis] if active else None

                self.x = axis if active else None
                self.pos.bind_left(pos_control)
                self.target.bind_left(target_control)
            return setter

        def set_y_for(axis):
            def setter(active):
                pos_control = pos.poss[axis] if active else None
                target_control = pos.targets[axis] if active else None

                self.y = axis if active else None
                self.pos.bind_right(pos_control)
                self.target.bind_right(target_control)
            return setter

        def get_x_for(axis):
            return lambda: self.x == axis

        def get_y_for(axis):
            return lambda: self.y == axis

        for label, axis in axes.items():
            x = Control('/2dpad/x/' + label, feedback=True, action=set_x_for(axis), source=get_x_for(axis))
            y = Control('/2dpad/y/' + label, feedback=True, action=set_y_for(axis), source=get_y_for(axis))
            setattr(self, 'btn_x' + label, x)
            setattr(self, 'btn_y' + label, y)


xy = XY('2dpad')

class Breath(Page):

    def update_sync(self, v):
        if v:
            self.r.freq = self.l.freq

    def update_phase(self, v):
        if not self.sync(): 
            return

        self.r.phase = self.l.phase + v


    def label_freq(self, hz):
        if hz >= 1.0:
            return "%.1f Hz" % hz

        return "%.1f s" % (1/hz)

    def toggle_for(self, lfo, axis):
        def toggle(value):
            if value:
                axis.lfos.add(lfo)
            else:
                axis.lfos.remove(lfo)

        return toggle

    def update_freq_for(self, axis):
        def update_freq(hz):
            if self.sync():
                self.l.freq = hz
                self.r.freq = hz
            else:
                axis.freq = hz
            
        return update_freq

    def update_bias_for(self, axis):
        def update_bias(bias):
            axis.center = bias

        return update_bias


    def init_controls(self):
        self.l = Axis.lfos[0]
        self.r = Axis.lfos[1]

        self.lamp = Control('/lfo/left/amplitude', (0, 30), action=lambda v: setattr(self.l, 'amp', v), mapping=Control.QUADRATIC)
        self.ramp = Control('/lfo/right/amplitude', (0, 30), action=lambda v: setattr(self.r, 'amp', v), mapping=Control.QUADRATIC)

        self.lfreq = Control('/lfo/left/frequency', (-5, 3), action=self.update_freq_for(self.l), source=Tracker(self.l, 'freq'), 
            mapping=Control.EXPONENTIAL)
        self.lfreql = Label('/lfo/left/label_frequency', self.lfreq, self.label_freq)
        self.rfreq = Control('/lfo/right/frequency', (-5, 3), action=self.update_freq_for(self.r), source=Tracker(self.r, 'freq'),
            mapping=Control.EXPONENTIAL)
        self.rfreql = Label('/lfo/right/label_frequency', self.rfreq, self.label_freq)

        self.lbias = Control('/lfo/left/bias', (0, 1), action=self.update_bias_for(self.l), source=Tracker(self.l, 'center'))
        self.rbias = Control('/lfo/right/bias', (0, 1), action=self.update_bias_for(self.r), source=Tracker(self.r, 'center'))

        self.lbiasr = Control('/lfo/left/bias_reset', action=lambda _: self.lbias.set(0.5))
        self.rbiasr = Control('/lfo/right/bias_reset', action=lambda _: self.rbias.set(0.5))

        self.lsine = Control('/lfo/left/sine', action=lambda _: self.lsaw.set(0))
        self.rsine = Control('/lfo/right/sine', action=lambda _: self.lsaw.set(0))

        self.sync = Control('/lfo/sync', action=self.update_sync, feedback=True)
        self.phase = Control('/lfo/phase', (-0.5, 0.5), action=self.update_phase)
        self.lphase = Label('/label_phase', self.phase, lambda v: "%.0f°" % (v*360))

        self.toggles = {}

        self.lfreq.set(1)
        self.rfreq.set(2)

        for label, axis in axes.items():
            toggle = Control('/lfo/left/' + label, action=self.toggle_for(self.l, axis), feedback=True)
            self.toggles['l_' + label] = toggle
            toggle = Control('/lfo/right/' + label, action=self.toggle_for(self.r, axis), feedback=True)
            self.toggles['r_' + label] = toggle


breath = Breath('lfo')

'''
class Mixer(Page):
    def controlled_axes(self):
        return [ax for ax, toggler in self.toggles.items() if toggler.get()]


    def set_for(self, base):
        def handler(_):
            print("%d controlled axes." % len(self.controlled_axes()))
            for ax in self.controlled_axes():
                print("setting at %f" % ax.position)
                base[ax] = ax.position
        return handler


    def go_for(self, base):
        if base is self.tl:
            x, y = 1, 0
        elif base is self.tr:
            x, y = 1, 1
        elif base is self.bl:
            x, y = 0, 0
        elif base is self.br:
            x, y = 0, 1

        def handler(_):
            for ax in self.controlled_axes():
                val = base[ax]
                if val is None:
                    print("Endpoint not set. Skipping...")
                ax.set_target(val)
                self.x.set(x)
                self.y.set(y)
        return handler


    def set_2d_target(self, x, y):
        ref_dist = 0  # the longest distance. Used to normalized all travel speeds

        targets = {}
        axes = self.controlled_axes()

        print(x)
        print(y)

        for ax in axes:
            cont = False
            if self.bl[ax] is None:
                print("BL is not defined")
                cont = True

            if self.br[ax] is None:
                print("BR is not defined")
                cont = True

            if self.tl[ax] is None:
                print("TL is not defined")
                cont = True

            if self.tr[ax] is None:
                print("TR is not defined")
                cont = True

            if cont: 
                continue

            rail_bot = self.bl[ax] + (self.br[ax] - self.bl[ax])*y
            rail_top = self.tl[ax] + (self.tr[ax] - self.tl[ax])*y
            target = rail_bot + (rail_top - rail_bot)*x
            targets[ax] = target

            dist = abs(target - ax.position)
            if dist > ref_dist:
                ref_dist = dist

        # The reference (ie. longest) distance is known now. Set speeds and targets:
        for ax in axes:
            target = targets[ax]
            dist = target - ax.position

            factor = abs(dist/ref_dist)

            ax.set_target(target)

            ax.restore_acc = ax.acc
            ax.restore_top_speed = ax.top_speed

            ax.acc = ax.acc*factor
            ax.top_speed = ax.top_speed*factor


    def init_controls(self):
        # Bases
        self.tl = {axis: None for axis in axes.values()}
        self.tr = {axis: None for axis in axes.values()}
        self.bl = {axis: None for axis in axes.values()}
        self.br = {axis: None for axis in axes.values()}

        self.toggles = {}
        for label, axis in axes.items():
            toggle = Control('/mixer/' + label, feedback=True)
            self.toggles[axis] = toggle

        self.acc = vel.acc
        self.vel_limit = vel.vel_limit

        self.set_tl = Control('/mixer/set/tl', action=self.set_for(self.tl))
        self.set_tr = Control('/mixer/set/tr', action=self.set_for(self.tr))
        self.set_bl = Control('/mixer/set/bl', action=self.set_for(self.bl))
        self.set_br = Control('/mixer/set/br', action=self.set_for(self.br))

        self.go_tl = Control('/mixer/go/tl', action=self.go_for(self.tl))
        self.go_tr = Control('/mixer/go/tr', action=self.go_for(self.tr))
        self.go_bl = Control('/mixer/go/bl', action=self.go_for(self.bl))
        self.go_br = Control('/mixer/go/br', action=self.go_for(self.br))

        self.x = Control('/mixer/x')
        self.y = Control('/mixer/y')
        self.target = ControlTuple('/mixer/target', action=self.set_2d_target, left=self.x, right=self.y)

mixer = Mixer('mixer')
'''


pages = [
    vel,
    pos,
    xy,
    breath
    #mixer
]

mem("pages")

active_page = pages[0]

def osc_handler(timetag, data):
    topic, tags, args, src = data

    values = args if args else None

    if values and len(values) == 1:
        print("(%d) %s -> %3.2f" % (len(args), topic, values[0]) )

    if topic == '/ping':
        global osc_client

        if osc_client:
            if not src == osc_client.dest:
                print('Ping received from new Address %s:%d, but ignored:' % src)
                print('GUI already bound to %s:%d.' % osc_client.dest)
            return

        print('Ping received. Binding GUI to %s:%d' % src)
        osc_client = Client(*src)

        # Switch to page 'velocity'
        bundle = Bundle()
        bundle.add(create_message('/page/velocity', 1))
        osc_client.send(bundle)

        # Signal.
        vel.fan.set(1)
        time.sleep_ms(500)
        vel.fan.set(0)

        return

    if topic.startswith('/page/'):
        global active_page
        page_id = topic[6:]
        matches = [page for page in pages if page.id == page_id]
        if len(matches) == 1:
            active_page = matches[0]

        else:
            print("Unknown or ambiguous page id %s." % page_id)

        print("Switching to page %s." % page_id)

        gui_update()
        return

    # Dispatch value updates
    for page in pages:
        for control in page.controls:
            control.pull(topic, values)


@rate_limit(25)
def gui_update(_=None):
    if not osc_client:
        return

    bundle = active_page.collect_updates()
    if bundle:
        gc.collect()
        #print("Bundle with %d msg." % len(bundle) )
        osc_client.send(bundle)


gui_timer = Timer(0)
gui_timer.init(period=200, mode=Timer.PERIODIC, callback=gui_update)

mem("gui callbacks")

if __name__ == '__main__':
    local = ap.ifconfig()[0]
    loop = get_event_loop()
    loop.call_soon(run_server(local, 8000, serve, dispatch=osc_handler))
    try:
        print('Ready for WIFI connection.')
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
