"""PV-Clean Rain v2.2 — pin map for Raspberry Pi Model B (2011.12).

Only BCM pins that are identical on Rev 1 and Rev 2 are used.
Check revision first:  grep Revision /proc/cpuinfo
  0002/0003 -> Rev 1 (I2C bus 0), 0004..000f -> Rev 2 (I2C bus 1)
See docs/04-design-v2.2-final.md, section 10.
"""

# Drive: 2x TB6612FNG, one per side, channels A+B wired in parallel (front+rear motor)
L_PWM, L_IN1, L_IN2 = 18, 23, 24
R_PWM, R_IN1, R_IN2 = 17, 22, 25

# Hardware watchdog: square wave -> charge pump -> STBY of both TB6612.
# Signal missing > ~100 ms => motors unpowered.
WD_HEARTBEAT = 4
WD_FREQ_HZ = 200

# Encoders (channel A only; direction known from command)
ENC_L, ENC_R = 7, 8

# Power: TPL5110 DONE pin (high = "finished", cuts Pi power)
TPL_DONE = 11

# Rain sensor digital out (disable serial console first)
RAIN_DO = 15

# I2C
I2C_BUS = 1          # set 0 on Rev 1 boards
MUX_ADDR = 0x70      # TCA9548A
MPU_ADDR = 0x68      # MPU-6050
INA_MOTOR = 0x40     # INA219 on D4004 Out1 -> VMOT
INA_CHARGE = 0x41    # INA219 on dock contacts -> D4004 input
TOF_CH = {"FL": 0, "FR": 1, "RL": 2, "RR": 3, "FWD": 4}  # VL53L0X on mux channels

# Geometry / logic (mm, m/s)
TOF_LEAD_MM = 120          # sensor ahead of / behind axle
GLASS_DIST_MM = 25         # nominal ToF reading on glass
DROP_THRESHOLD_MM = 30     # reading > glass + this => "no glass"
GAP_MAX_TRAVEL_MM = 60     # glass must return within this travel, else EDGE
EDGE_SWEEP_MM = 55         # extra travel at bottom edge (wiper over frame lip)
LANE_PITCH_MM = 180
V_CLEAN, V_RETURN, V_DOCK = 0.06, 0.08, 0.03
