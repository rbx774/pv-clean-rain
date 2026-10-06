#!/usr/bin/env python3
"""Test A (v0.2): 4WD drive check on the wet 16-degree mock board.

Supervised bench use only - no edge logic yet.
Starts the watchdog heartbeat (keeps TB6612 STBY high), ramps up, drives,
ramps down. Ctrl-C or any crash stops the heartbeat -> motors unpowered.

Usage: python3 crawl_v01.py [forward|backward] [seconds] [speed 0..1]
Recommended pin factory: sudo pigpiod; export GPIOZERO_PIN_FACTORY=pigpio
"""
import sys
import time

from gpiozero import Motor, PWMOutputDevice

import config as cfg


def ramp(left, right, target, direction, steps=20, dt=0.05):
    for i in range(1, steps + 1):
        s = target * i / steps
        getattr(left, direction)(s)
        getattr(right, direction)(s)
        time.sleep(dt)


def main():
    direction = sys.argv[1] if len(sys.argv) > 1 else "forward"
    seconds = float(sys.argv[2]) if len(sys.argv) > 2 else 3.0
    speed = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
    assert direction in ("forward", "backward")

    heartbeat = PWMOutputDevice(cfg.WD_HEARTBEAT, frequency=cfg.WD_FREQ_HZ, initial_value=0.5)
    left = Motor(forward=cfg.L_IN1, backward=cfg.L_IN2, enable=cfg.L_PWM, pwm=True)
    right = Motor(forward=cfg.R_IN1, backward=cfg.R_IN2, enable=cfg.R_PWM, pwm=True)
    try:
        time.sleep(0.2)  # let charge pump raise STBY
        ramp(left, right, speed, direction)
        time.sleep(seconds)
        ramp(left, right, 0.0, direction, steps=10)
    finally:
        left.stop()
        right.stop()
        heartbeat.off()  # STBY drops -> driver outputs off


if __name__ == "__main__":
    main()
