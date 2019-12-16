from micropython import const
from math import log, sqrt
from uosc.client import Client, Bundle, create_message
import utime

class Control:
    ''' A value controller with value/scale mapping. Tracks changes and pushes updates selectively to the OSC remote. '''

    LINEAR = const(0)
    QUADRATIC = const(1)
    EXPONENTIAL = const(2)

    def __init__(self, topic, span=(0, 1), mapping=LINEAR, action=None, feedback=False, source=None):
        self.topic = topic
        self.mapping = mapping
        self.action = action
        self.feedback = feedback
        self.val = source  # is either a value cache or a callback

        self.lower, self.upper = span
        self.bidi = False

        if self.lower is None:
            # Automaticly generate symmetric span
            self.bidi = True

        elif self.lower < 0:
            # Check bidirectional spans for symmetricity
            if self.mapping != Control.EXPONENTIAL and abs(self.lower) != self.upper:
                raise ValueError("Bidirectional spans must be symmetric")
            self.bidi = True

        self._gui_value = None
        self._previous_bounds = None

        if not self.val:
            self.val = 0 if self.bidi else self._bounds()[0]


    def __call__(self):
        return self.get()


    def get(self):
        ''' Fetch the current value of this control (may depend on peripherals). '''
        if callable(self.val):
            return self.val()
        return self.val


    def set(self, value):
        ''' Set the current value of this control and trigger handlers. '''

        if not callable(self.val):
            self.val = value

        if self.action:
            self.action(value)


    def push(self):
        ''' Create an OSC message if changes are pending. '''
        value = self.get()
        bounds = self._bounds()
        if value == self._gui_value and bounds == self._previous_bounds:
            return None

        self._gui_value = value  # Clear dirty flag.
        self._previous_bounds = bounds
        return (create_message(self.topic, self._pack(value)),)


    def mark_dirty(self):
        ''' Forces a value resend on the next #push. '''
        self._gui_value = None


    def pull(self, topic, values):
        ''' Update this controls value from an OSC message. '''
        if self.topic != topic:
            return

        value = self._unpack(values[0])

        if not self.feedback:
            self._gui_value = value
        # With feedback = True, the pending difference will cause a new message on the next #push

        if self.feedback and not callable(self.val) and value == self.val:
            # A new requested value is identical to the current one. Most likely,
            # the GUI is out of sync due to a lost UDP-packet. As hacky fix, the
            # GUI value cache is reset to trigger a resend.
            self._gui_value = None

        self.set(value)


    def _bounds(self):
        upper = self.upper() if callable(self.upper) else self.upper

        if self.bidi:
            bounds = -upper, upper

        else:
            lower = self.lower() if callable(self.lower) else self.lower
            bounds = (lower, upper)

        return bounds


    def _pack(self, value):
        lower, upper = self._bounds()

        if self.mapping is Control.EXPONENTIAL:
            value = log(value)/log(2)

        value = (value - lower)/(upper - lower)
        if self.bidi:
            value = value*2 - 1
        # val e 0..1 or -1..1 if bidi

        if self.mapping is Control.QUADRATIC:
            sign = 1 if value > 0 else -1
            value = sign*sqrt(abs(value))

        return value


    def _unpack(self, value):
        lower, upper = self._bounds()

        if self.mapping is Control.QUADRATIC:
            value = value*abs(value)

        # value e 0..1 or -1..1 if bidi
        if self.bidi:
            value = (value + 1)/2

        value = value*(upper - lower) + lower

        if self.mapping is Control.EXPONENTIAL:
            value = 2**value

        return value


class ControlTuple:
    def __init__(self, topic, action=None, left=None, right=None):
        self.topic = topic
        self.left = left
        self.right = right

        self._gui_values = (None, None)

        def action_fallback(l, r):
            self.left.set(l) if self.left else None
            self.right.set(r) if self.right else None

        self.action = action if action else action_fallback


    def __call__(self):
        return self.get()


    def get(self):
        l = self.left.get() if self.left else None
        r = self.right.get() if self.right else None
        return (l, r)


    def set(self, l, r):
        self.action(l, r)

        ''' actually, this class does not even to have an inner state?
        self.left.set(l) if self.left else None
        self.right.set(r) if self.right else None
        '''


    def push(self):
        values = self.get()
        if values == self._gui_values:
            return None

        self._gui_values = values  # Clear dirty flag.
        l = self.left._pack(values[0]) if self.left else 0
        r = self.right._pack(values[1]) if self.right else 0
        return (create_message(self.topic, l, r),)


    def mark_dirty(self):
        ''' Forces a value resend on the next #push. '''
        self._gui_values = None


    def pull(self, topic, values):
        if self.topic != topic:
            return

        l = self.left._unpack(values[0]) if self.left else None
        r = self.right._unpack(values[1]) if self.right else None

        self.set(l, r)


    def bind_left(self, left):
        self.left = left
        self._gui_values = (None, None)


    def bind_right(self, right):
        self.right = right
        self._gui_values = (None, None)



class Tracker:
    def __init__(self, obj, attr):
        self.obj = obj
        self.attr = attr
        self.cache = None


    def __call__(self):
        return self.get()


    def get(self):
        self.cache = getattr(self.obj, self.attr)
        return self.cache

    # TODO brauchts das cache überhaupt?


class Label:
    def __init__(self, topic, source, formatter):
        self.topic = topic
        self.source = source

        if callable(formatter):
            self.formatter = formatter
        elif isinstance(formatter, str):
            # Interpret as format string
            self.formatter = lambda v: formatter % v
        else:
            raise ValueError("formatter must be either a function or a format string")

        self._gui_label = None


    def push(self):
        ''' Create an OSC message if changes are pending. '''
        value = self.source()
        label = self.formatter(value)

        if label == self._gui_label:
            return None

        self._gui_label = label  # Clear dirty flag.
        return (create_message(self.topic, label),)


    def mark_dirty(self):
        ''' Forces a value resend on the next #push. '''
        self._gui_label = None


    def pull(self, topic, values):
        pass


class Page:
    def __init__(self, id, *controls):
        self.id = id
        if not hasattr(self, 'init_controls'):
            raise ValueError("Subclass does not implement #init_controls!")

        self.init_controls()

        self.controls = set()
        for name in dir(self):
            attr = getattr(self, name)
            if isinstance(attr, Control) or isinstance(attr, ControlTuple) or isinstance(attr, Label):
                self.controls.add(attr)

            if isinstance(attr, dict):
                for item in attr.values():
                    if isinstance(item, Control) or isinstance(item, ControlTuple):
                        self.controls.add(item)


    def add(self, *args):
        self.controls.union(set(args))


    def collect_updates(self):
        bundle = Bundle()
        for control in self.controls:
            updates = control.push()
            if updates:
                bundle.add(*updates)

        return bundle


def rate_limit(ms):
    def decorate(func):
        last_update = 0
        def rate_limited_function(*args, **kargs):
            nonlocal last_update
            if utime.ticks_ms() - last_update < ms:
                return

            ret = func(*args, **kargs)
            last_update = utime.ticks_ms()
            return ret
        return rate_limited_function
    return decorate
