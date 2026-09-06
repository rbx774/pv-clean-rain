#!/usr/bin/env python3
"""Minimal agent-side client for the ESP32 JSON serial API.
Swap serial for BLE later; keep the same commands for agentic tools.
"""
from __future__ import annotations

import argparse
import json
import sys

try:
    import serial
except ImportError:
    print("pip install pyserial", file=sys.stderr)
    raise


def send(ser: serial.Serial, payload: dict) -> dict:
    ser.write((json.dumps(payload) + "\n").encode())
    line = ser.readline().decode().strip()
    return json.loads(line) if line else {"ok": False, "err": "empty"}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--port", required=True)
    p.add_argument("--baud", type=int, default=115200)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("ping")
    sub.add_parser("status")
    sub.add_parser("stop")
    s = sub.add_parser("start_row")
    s.add_argument("--speed", type=float, default=0.35)
    args = p.parse_args()

    with serial.Serial(args.port, args.baud, timeout=2) as ser:
        if args.cmd == "ping":
            print(send(ser, {"cmd": "ping"}))
        elif args.cmd == "status":
            print(send(ser, {"cmd": "status"}))
        elif args.cmd == "stop":
            print(send(ser, {"cmd": "stop"}))
        elif args.cmd == "start_row":
            print(send(ser, {"cmd": "start_row", "speed": args.speed}))


if __name__ == "__main__":
    main()
