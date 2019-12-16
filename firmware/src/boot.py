# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import webrepl
webrepl.start()

import esp
import network

from micropython import opt_level, alloc_emergency_exception_buf
opt_level(1)  # avoid __debug__-clauses. They are only supported by the unix port of micropython.
#alloc_emergency_exception_buf(100)

esp.osdebug(0)  # debug to uart

ap = network.WLAN(network.AP_IF)
ap.active(True)
#ap.config(essid='koebi', authmode=network.AUTH_WPA2_PSK, password='N7j4sk***', channel=11)
ap.config(essid='koebi', channel=8)

