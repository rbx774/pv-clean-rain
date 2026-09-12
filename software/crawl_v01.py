#!/usr/bin/env python3
"""v0.1 — differential drive + IR edge hard-stop for PV-Clean Rain on Pi 2011.12."""
from __future__ import annotations

import time
from gpiozero import DigitalInputDevice, DigitalOutputDevice, Button

import config as cfg


class HBridgeSide:
    def __init__(self, in1: int, in2: int):
        self.a = DigitalOutputDevice(in1, initial_value=False)
        self.b = DigitalOutputDevice(in2, initial_value=False)

    def stop(self) -> None:
        self.a.off()
        self.b.off()

    def forward(self) -> None:
        self.a.on()
        self.b.off()

    def reverse(self) -> None:
        self.a.off()
        self.b.on()


def main() -> None:
    left = HBridgeSide(cfg.MOTOR_L_IN1, cfg.MOTOR_L_IN2)
    right = HBridgeSide(cfg.MOTOR_R_IN1, cfg.MOTOR_R_IN2)
    # TCRT DO often HIGH = surface present — invert if your module differs
    ir_l = DigitalInputDevice(cfg.IR_FRONT_L, pull_up=True)
    ir_r = DigitalInputDevice(cfg.IR_FRONT_R, pull_up=True)
    estop = Button(cfg.ESTOP_BTN, pull_up=True)

    def all_stop() -> None:
        left.stop()
        right.stop()

    print("crawl_v01: space=forward stop on edge/estop; Ctrl+C quit")
    try:
        while True:
            if estop.is_pressed or (not ir_l.value) or (not ir_r.value):
                all_stop()
                time.sleep(0.02)
                continue
            left.forward()
            right.forward()
            time.sleep(0.02)
    except KeyboardInterrupt:
        all_stop()
        print("stopped")


if __name__ == "__main__":
    main()
